import asyncio
import grpc
import sys
import traceback
import uuid
from abc import ABC
from collections import defaultdict
from contextlib import asynccontextmanager
from google.protobuf.descriptor_pb2 import FileDescriptorSet
from google.protobuf.message import Message
from resemble.aio.contexts import (
    Context,
    Participants,
    ReaderContext,
    TransactionContext,
    WriterContext,
)
from resemble.aio.internals.channel_manager import _ChannelManager
from resemble.aio.internals.middleware import Middleware
from resemble.aio.internals.tasks_dispatcher import TasksDispatcher
from resemble.aio.tasks import TaskEffect
from resemble.aio.types import ActorId, ServiceName
from resemble.consensus.service_descriptor_validator import (
    validate_descriptor_sets_are_backwards_compatible,
)
from resemble.consensus.sidecar import SidecarClient
from resemble.consensus.sidecar_native import SidecarServer
from resemble.v1alpha1 import (
    sidecar_pb2,
    tasks_pb2,
    transactions_pb2,
    transactions_pb2_grpc,
)
from tempfile import TemporaryDirectory
from typing import AsyncIterator, Awaitable, Callable, Optional, Tuple


class Effects:
    """Helper class that captures all the possible effects a method might
    have.
    """

    def __init__(
        self,
        *,
        state: Message,
        response: Optional[Message] = None,
        tasks: Optional[list[TaskEffect]] = None
    ):
        self.state = state
        self.response = response
        self.tasks = tasks


class StateManager(ABC):
    """Base class for all state managers.

    State managers are used by the middleware to provide access to the
    underlying state.
    """

    class Writer:
        """Helper class that ensures all attempts to store state come from
        using 'StateManager.writer(...)'.
        """

        def __init__(self, complete: Callable[[Effects], Awaitable[None]]):
            self._complete = complete

        async def complete(self, effects: Effects) -> None:
            await self._complete(effects)

    class TaskReader:
        """Helper class for running tasks that are readers.
        """

        def __init__(
            self, complete: Callable[[TaskEffect, Message], Awaitable[None]]
        ):
            self._complete = complete

        async def complete(self, task: TaskEffect, response: Message) -> None:
            await self._complete(task, response)

    class TaskWriter:
        """Helper class for running tasks that are writers.
        """

        def __init__(
            self, complete: Callable[[TaskEffect, Effects], Awaitable[None]]
        ):
            self._complete = complete

        async def complete(self, task: TaskEffect, effects: Effects) -> None:
            await self._complete(task, effects)

    class Transaction:
        """Helper class for managing ongoing transaction state.

        As a helper some members of the class are meant to be accessed
        directly, while others are meant to be accessed by methods.

        The methods are not meant to do anything complicated, but
        instead just provide syntactic sugar to simplify updating
        transaction state throughout the code. The one exception to
        that is that we've made the class awaitable to make it easy to
        wait for an ongoing transaction to finish (either aborted or
        committed) in the code.
        """

        @classmethod
        def from_context(
            cls,
            context: Context,
            tasks_dispatcher: TasksDispatcher,
        ):
            assert context.transaction_id is not None
            assert context.transaction_coordinator_service is not None
            assert context.transaction_coordinator_actor_id is not None
            return cls(
                transaction_id=context.transaction_id,
                coordinator_service=context.transaction_coordinator_service,
                coordinator_actor_id=context.transaction_coordinator_actor_id,
                service=context.service_name,
                actor_id=context.actor_id,
                tasks_dispatcher=tasks_dispatcher,
                idempotency_key=context.idempotency_key,
            )

        @classmethod
        def from_sidecar(
            cls,
            transaction: sidecar_pb2.Transaction,
            middleware: Middleware,
        ):
            return cls(
                transaction_id=uuid.UUID(bytes=transaction.transaction_id),
                coordinator_service=transaction.coordinator_service,
                coordinator_actor_id=transaction.coordinator_actor_id,
                service=transaction.service,
                actor_id=transaction.actor_id,
                tasks_dispatcher=middleware.tasks_dispatcher,
                stored=True,
                prepared=transaction.prepared,
                # During recovery any transactions that were not
                # prepared must abort because rocksdb only persists
                # transactions that have been prepared.
                must_abort=not transaction.prepared,
                tasks=[
                    TaskEffect.from_sidecar_task(
                        task,
                        middleware.request_type_by_method_name[task.method],
                    ) for task in transaction.uncommitted_tasks
                ],
                idempotent_mutations={
                    uuid.UUID(bytes=idempotent_mutation.key):
                        idempotent_mutation for idempotent_mutation in
                    transaction.uncommitted_idempotent_mutations
                },
            )

        def __init__(
            self,
            *,
            transaction_id: uuid.UUID,
            coordinator_service: ServiceName,
            coordinator_actor_id: ActorId,
            service: ServiceName,
            actor_id: ActorId,
            tasks_dispatcher: TasksDispatcher,
            stored: bool = False,
            prepared: bool = False,
            must_abort: bool = False,
            tasks: Optional[list[TaskEffect]] = None,
            idempotency_key: Optional[uuid.UUID] = None,
            idempotent_mutations: Optional[dict[uuid.UUID,
                                                sidecar_pb2.IdempotentMutation]
                                          ] = None,
        ):
            self.id = transaction_id
            self.coordinator_service = coordinator_service
            self.coordinator_actor_id = coordinator_actor_id
            self.service = service
            self.actor_id = actor_id

            self.idempotency_key = idempotency_key

            self.idempotent_mutations = idempotent_mutations or {}

            self.tasks_dispatcher = tasks_dispatcher

            # Lock to provide atomicity for updating some of the
            # members, e.g., 'stored'.
            self.lock = asyncio.Lock()

            # Whether or not the transaction has been stored in the
            # sidecar and thus we are officially a participant. Should
            # be read/written only when holding 'lock'. Use property
            # `self.stored` to access this safely.
            self._stored = stored

            # Whether or not we should abort this transaction when
            # asked by the coordinator.
            self.must_abort = False

            # Provisional actor state within the transaction.
            self.state: Optional[Message] = None

            # Streaming readers executing within this transaction.
            #
            # An entry in the queue is a tuple of (state,
            # idempotency_key) where 'idempotency_key' may be None.
            self.streaming_readers: list[asyncio.Queue[Optional[Tuple[
                Message, Optional[uuid.UUID]]]]] = []

            # Aggregated tasks that should be dispatched if this
            # transaction commits.
            self.tasks = tasks or []

            assert all(
                task.task_id.service == self.service for task in self.tasks
            ), 'Transaction contains tasks not belonging to transaction'

            # asyncio.Task for the "watch control loop" which watches
            # the coordinator for updates about the transaction, i.e.,
            # if it was aborted or has been committed.
            self.watch_task: Optional[asyncio.Task] = None

            # Whether or not the transaction has been prepared.
            self._prepared = prepared

            # Whether or not the transaction was committed.
            self._committed: asyncio.Future[bool] = asyncio.Future()

        @property
        def stored(self) -> bool:
            """Getter to attribute `_stored` that checks that lock is held and
            that the attribute is safe to access."""
            assert self.lock.locked()
            return self._stored

        @stored.setter
        def stored(self, value: bool) -> None:
            """Setter to attribute `_stored` that checks that lock is held and
            that the attribute can be safely set."""
            assert self.lock.locked()
            self._stored = value

        def prepare(self) -> None:
            """Marks the transaction as prepared."""
            assert not self._prepared, 'Prepare should only happen once!'
            self._prepared = True

        def prepared(self) -> bool:
            """Returns whether or not the transaction is prepared."""
            return self._prepared

        def commit(self) -> None:
            """Marks the transaction as committed. Must first be prepared."""
            assert self.prepared()

            # NOTE: invariant is that after setting '_committed' we
            # WILL NOT RAISE, otherwise we won't be able to retry
            # to commit since 'finished()' will return true.
            self._committed.set_result(True)

        def abort(self) -> None:
            """Marks the transaction as aborted."""
            # NOTE: invariant is that after setting '_committed' we
            # WILL NOT RAISE, otherwise we won't be able to retry
            # to abort since 'finished()' will return true.
            self._committed.set_result(False)

        def __await__(self):
            """Awaits for transaction to finish, i.e., aborted or committed."""

            async def closure():
                await self._committed

            return closure().__await__()

        def committed(self) -> bool:
            """Returns whether or not the transaction is committed."""
            if self._committed.done():
                return self._committed.result()
            else:
                return False

        def aborted(self) -> bool:
            """Returns whether or not the transaction is aborted."""
            if self._committed.done():
                return not self._committed.result()
            else:
                return False

        def finished(self) -> bool:
            """Returns whether or not the transaction is finished."""
            return self._committed.done()

    def add_to_server(self, server: grpc.aio.Server) -> None:
        """Hook for adding the state manager to a gRPC server."""
        raise NotImplementedError()

    @asynccontextmanager
    async def transactionally(
        self,
        context: ReaderContext | WriterContext | TransactionContext,
        tasks_dispatcher: TasksDispatcher,
    ) -> AsyncIterator[Optional[Transaction]]:
        """Performs any necessary set up to execute the body of the context
        manager transactionally. The body may be for a reader, a
        writer, or a transaction itself.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def reader(self, context: ReaderContext,
                     state_type: type[Message]) -> AsyncIterator[Message]:
        """Helper that handles code generated readers. Loads and returns the
        state for the actor specified in the context.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def streaming_reader(
        self, context: ReaderContext, state_type: type[Message]
    ) -> AsyncIterator[AsyncIterator[Message]]:
        """Helper that handles code generated streaming readers. Loads an
        async iterator of states for the actor specified in the
        context.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def streaming_reader_idempotency_key(
        self, context: ReaderContext, state_type: type[Message]
    ) -> AsyncIterator[AsyncIterator[Tuple[Message, Optional[uuid.UUID]]]]:
        """Loads an async iterator of states and the idempotency keys that
        caused that state update.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def writer(
        self,
        context: WriterContext,
        state_type: type[Message],
        *,
        transaction: Optional[Transaction] = None,
        from_constructor: bool = False,
        requires_constructor: bool = False
    ) -> AsyncIterator[Tuple[Message, Writer]]:
        """Helper that handles code generated writers. Loads the state,
        performing any necessary functionality to ensure only one
        writer at a time, for the actor specified in the context.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def task_reader(
        self, context: ReaderContext, state_type: type[Message]
    ) -> AsyncIterator[Tuple[Message, TaskReader]]:
        """Helper that handles code generated task readers. Loads the state
        for the actor specified in the context.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def task_writer(
        self, context: WriterContext, state_type: type[Message]
    ) -> AsyncIterator[Tuple[Message, TaskWriter]]:
        """Helper that handles code generated task writers. Loads the state,
        performing any necessary functionality to ensure only one
        writer at a time, for the actor specified in the context.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    @asynccontextmanager
    async def transaction(
        self,
        context: TransactionContext,
        state_type: type[Message],
        transaction: Transaction,
        *,
        from_constructor: bool = False,
        requires_constructor: bool = False
    ) -> AsyncIterator[Callable[[Message], Awaitable[None]]]:
        """Helper that handles code generated transactions. Performs necessary
        functionality to execute the transaction for the actor
        specified in the context.
        """
        raise NotImplementedError()
        yield  # Necessary for type checking.

    def get_response_if_idempotent_mutation(
        self,
        context: WriterContext | TransactionContext,
    ) -> Optional[bytes]:
        """Helper for code generated writers and transactions that returns the
        serialized response if the mutation has been performed or None
        if the mutation has not been performed.
        """
        raise NotImplementedError()

    async def load_task_response(
        self,
        task_id: tasks_pb2.TaskId,
    ) -> Optional[bytes]:
        """Loads the response for the given task. Returns None if the task is
        not yet complete. Throws if the task ID is not recognized.
        """
        raise NotImplementedError()

    async def read(
        self,
        context: TransactionContext,
        state_type: type[Message],
    ) -> Message:
        """Helper for reading the state within a transaction."""
        raise NotImplementedError()

    async def recover(
        self,
        channel_manager: _ChannelManager,
        middleware_by_service_name: dict[ServiceName, Middleware],
        file_descriptor_set: FileDescriptorSet,
    ) -> None:
        """Attempt to recover server state after a potential restart."""
        raise NotImplementedError()


class SidecarStateManager(
    StateManager,
    transactions_pb2_grpc.CoordinatorServicer,
    transactions_pb2_grpc.ParticipantServicer,
):
    """Implementation of state manager that stores data using the sidecar.

    SidecarStateManager also implements both the coordinator and
    participant interfaces for performing transactions.
    """

    def __init__(self, *, sidecar_address: str):
        self._sidecar_client = SidecarClient(sidecar_address)

        # TODO(benh): add a helper class, e.g., ActorData, that
        # encapsulates all of '_states', '_mutator_locks', etc.
        self._states: defaultdict[ServiceName,
                                  dict[ActorId,
                                       Message]] = defaultdict(lambda: {})

        # A "mutator" is either a writer or a transaction.
        self._mutator_locks: defaultdict[ServiceName, defaultdict[
            ActorId,
            asyncio.Lock]] = defaultdict(lambda: defaultdict(asyncio.Lock))

        # Transactions that actors of this state manager are
        # participating in.
        self._participant_transactions: defaultdict[ServiceName, dict[
            ActorId, StateManager.Transaction]] = defaultdict(lambda: {})

        # Map from transaction UUID to a Future indicating whether or
        # not the transaction has been prepared (and thus can be
        # committed) for all transactions being coordinated by this
        # state manager.
        #
        # TODO(benh): need to remove these from this list after some
        # expiration timeout, or better yet, run a control loop that
        # forever tries to complete the commit phase and only
        # afterwards removes this from the list (and from rocksdb).
        self._coordinator_prepared: dict[uuid.UUID, asyncio.Future[bool]] = {}

        # Coordinator "commit control loop" tasks for transactions
        # that have been prepared.
        self._coordinator_commit_control_loop_tasks: dict[uuid.UUID,
                                                          asyncio.Task] = {}

        # When a writer is invoked from within a transaction only we
        # will abstain from taking the mutator lock but we still
        # want to only execute one writer at a time which we ensure by
        # having each writer within a transaction take a sublock.
        self._transaction_writer_locks: defaultdict[ServiceName, defaultdict[
            ActorId,
            asyncio.Lock]] = defaultdict(lambda: defaultdict(asyncio.Lock))

        self._loads: defaultdict[ServiceName, dict[
            ActorId, asyncio.Event]] = defaultdict(lambda: {})

        # Any streaming readers. We're explicitly using a 'dict' as
        # the value instead of a 'defaultdict' because we don't want
        # to construct memory every time we "check" if there is a
        # queue of streaming readers. That could be a lot of empty
        # queues because we check for streaming readers on _every_
        # write!
        #
        # An entry in the queue is a tuple of (state, idempotency_key)
        # where 'idempotency_key' may be None.
        self._streaming_readers: defaultdict[ServiceName, dict[
            ActorId, list[asyncio.Queue[Optional[Tuple[
                Message, Optional[uuid.UUID]]]]]]] = defaultdict(lambda: {})

        # Idempotent mutations keyed by the idempotency key.
        self._idempotent_mutations: dict[uuid.UUID,
                                         sidecar_pb2.IdempotentMutation] = {}

    async def _load(
        self,
        context: Context,
        state_type: type[Message],
        *,
        from_reader: bool = False,
        from_constructor: bool = False,
        requires_constructor: bool = False
    ) -> Message:
        """Private helper for loading state from the sidecar.

        Code should use reader(), writer(), or streaming_reader(), not
        _load() directly.
        """
        service = context.service_name
        actor_id = context.actor_id

        transaction: Optional[StateManager.Transaction] = None

        if context.transaction_id is None:
            # When reading the state of an actor outside of a transaction while
            # a transaction is ongoing we always return the last committed state
            # (the latest "snapshot"). If, however, that ongoing transaction has
            # been prepared then its transaction coordinator may have
            # successfully run two phase commit and we just haven't heard about
            # it yet. In this case, it is possible that we receive a read
            # outside of a transaction that is expecting the actor to have the
            # state which has not yet been committed locally, and thus we must
            # wait for our local transaction to commit (or abort, but in that
            # case the read won't have been expecting the uncommitted state).
            # This avoids the race condition laid out in
            # https://github.com/reboot-dev/respect/issues/1621.
            #
            # NOTE: The `ongoing_transaction` is different from the
            # `transaction` variable above: the `transaction` variable is tied
            # to `context` (through `context.transaction_id`), while the
            # `ongoing_transaction` is an ongoing transaction on the actor that
            # the caller is not a participant of.
            ongoing_transaction: Optional[
                StateManager.Transaction
            ] = self._participant_transactions[service].get(actor_id)
            if ongoing_transaction is not None and ongoing_transaction.prepared(
            ):
                # There is a transaction ongoing, and it has been prepared. We
                # need to wait for it to complete.
                try:
                    await ongoing_transaction
                except:
                    # Any errors coming from the transaction do not concern us
                    # here.
                    pass
        else:
            transaction = self._participant_transactions[service].get(actor_id)
            assert transaction is not None and not transaction.prepared(
            ) and not transaction.finished(
            ) and context.transaction_id == transaction.id, (
                f"Transaction '{str(context.transaction_id)}' missing "
                f"for service '{service}' and actor '{actor_id}'"
            )

        state: Optional[Message] = self._states[service].get(actor_id)
        if transaction is not None:
            # Need to set transaction state if this is the first time
            # doing a load within a transaction for this actor.
            if transaction.state is None and state is not None:
                transaction.state = state
            state = transaction.state

        if state is not None and from_constructor:
            raise ValueError(
                'Invoking constructor of already constructed actor'
            )
        elif state is not None:
            return state
        else:
            # We don't have state cached, so attempt to load it from
            # the sidecar. This will return None if state has not
            # (yet) been stored.
            #
            # To avoid multiple readers or a reader/writer trying to
            # load the state at the same time, we use a "load" event
            # which once triggered implies the state has been loaded.
            #
            # We are specifically _not_ using the actor lock because a
            # writer will have already acquired the lock at this point
            # (see the 'writer()' method below) and _will not release_
            # the lock until some later point (e.g., after it has
            # serviced the RPC) which will hold up other readers! Once
            # the state is loaded we want all the readers to be able
            # to begin execution immediately.
            load = self._loads[service].get(actor_id)
            if load is None:
                load = asyncio.Event()
                self._loads[service][actor_id] = load

                try:
                    data: Optional[
                        bytes] = await self._sidecar_client.load_actor_state(
                            service, actor_id
                        )

                    if data is not None:
                        if from_constructor:
                            raise ValueError(
                                'Invoking constructor of already '
                                'constructed actor'
                            )

                        state = state_type()
                        state.ParseFromString(data)
                        self._states[service][actor_id] = state

                        if transaction is not None:
                            transaction.state = state

                        # Need to enqueue the loaded state to any
                        # outstanding queues; see comments in
                        # 'streaming_reader()' for more details.
                        #
                        # Note that even though enqueuing requires
                        # doing an 'await' which means we might yield
                        # to the event loop, because we don't trigger
                        # the 'load' event until _after_ we're done
                        # with all the queues we know that we'll get
                        # all future state updates. That is, if it's a
                        # reader (or streaming reader) that is doing
                        # the loading then a writer will be waiting
                        # for the 'load' event. Meanwhile if it is a
                        # writer doing the loading then it will do all
                        # the enqueuing before even returning from
                        # this function.
                        queues: Optional[list[asyncio.Queue[
                            Optional[Tuple[Message, Optional[uuid.UUID]]]
                        ]]] = self._streaming_readers[service].get(actor_id)

                        if queues is not None:
                            for queue in queues:
                                # NOTE: we defer making a reader
                                # specific copy of this state until
                                # the reader actually reads it to
                                # reduce memory usage.
                                queue.put_nowait((state, None))

                        if transaction is not None:
                            for queue in transaction.streaming_readers:
                                # NOTE: we defer making a reader
                                # specific copy of this state until
                                # the reader actually reads it to
                                # reduce memory usage.
                                queue.put_nowait((state, None))

                        return state
                    elif requires_constructor and not from_constructor:
                        raise ValueError(
                            'Must use a constructor to construct a new actor'
                        )
                    elif from_reader:
                        raise ValueError(
                            'Must use a writer or constructor to construct a new actor'
                        )
                    else:
                        return state_type()
                finally:
                    # Trigger anyone waiting on the load. Note that it
                    # doesn't matter whether or not we were actually
                    # able to load any state; no matter what we want
                    # all coroutines waiting on the load to resume.
                    del self._loads[service][actor_id]
                    load.set()
            else:
                # We'll wait for the load and then recursively try
                # again in the event that the loader failed (e.g.,
                # perhaps the loader was from a reader and the
                # actor had not yet been constructed but we're a
                # writer and will successfully be able to load).
                await load.wait()
                return await self._load(
                    context,
                    state_type,
                    from_reader=from_reader,
                    from_constructor=from_constructor,
                    requires_constructor=requires_constructor
                )

    async def _store(
        self,
        *,
        service: ServiceName,
        actor_id: ActorId,
        effects: Optional[Effects] = None,
        transaction: Optional[StateManager.Transaction] = None,
        completed_task: Optional[sidecar_pb2.Task] = None,
        idempotency_key: Optional[uuid.UUID] = None,
        response: Optional[Message] = None,
    ):
        """Private helper for storing state from the sidecar.

        Code should use writer(), not _store() directly.
        """
        task_upserts: list[sidecar_pb2.Task] = []
        actor_upserts: list[sidecar_pb2.Actor] = []

        # NOTE: to be safe, we create a copy of state in case a
        # reference to it somehow is being held (e.g., in a coroutine
        # that the user didn't realize) and it gets modified while the
        # sidecar is storing it but before we add it to the streaming
        # readers queues below.
        state_copy: Optional[Message] = None

        if effects is not None:
            # Invariant for storing actor state is that the caller
            # holds the mutator actor lock!
            #
            # TODO(benh): better yet would be to check that the current
            # asyncio context holds the lock ... maybe use a contextvar?
            assert self._mutator_locks[service][actor_id].locked()

            state_copy = type(effects.state)()
            state_copy.CopyFrom(effects.state)

            actor_upserts.append(
                sidecar_pb2.Actor(
                    service=service,
                    actor_id=actor_id,
                    state=state_copy.SerializeToString()
                )
            )

            if effects.tasks is not None:
                task_upserts += [
                    task_effect.to_sidecar_task()
                    for task_effect in effects.tasks
                ]

        if completed_task is not None:
            task_upserts.append(completed_task)

        idempotent_mutation: Optional[sidecar_pb2.IdempotentMutation] = None

        # If we've been passed an idempotency key then we must have a
        # response that we need to store as well, but it may have been
        # passed explicitly or it may be within 'effects'.
        if idempotency_key is not None:
            if response is None:
                assert effects is not None
                assert effects.response is not None
                response = effects.response
            else:
                assert effects is None or effects.response is None

            idempotent_mutation = sidecar_pb2.IdempotentMutation(
                key=idempotency_key.bytes,
                response=response.SerializeToString(),
            )

        # NOTE: we _must_ store the data in the sidecar _before_
        # updating in memory state in case the store fails.
        await self._sidecar_client.store(
            actor_upserts,
            task_upserts,
            sidecar_pb2.Transaction(
                service=service,
                actor_id=actor_id,
                transaction_id=transaction.id.bytes,
                coordinator_service=transaction.coordinator_service,
                coordinator_actor_id=transaction.coordinator_actor_id,
            ) if transaction is not None else None,
            idempotent_mutation,
        )

        # Now that everything is stored we can update in memory
        # state. First we update state related to effects (if any).
        if effects is not None:
            assert state_copy is not None

            queues: Optional[list[asyncio.Queue[Optional[Tuple[
                Message, Optional[uuid.UUID]]]]]] = None

            if transaction is not None:
                transaction.state = state_copy
                queues = transaction.streaming_readers
            else:
                self._states[service][actor_id] = state_copy
                queues = self._streaming_readers[service].get(actor_id)

            if queues is not None:
                for queue in queues:
                    # NOTE: we defer making a reader specific copy of this
                    # state until the reader actually reads it to reduce
                    # memory usage.
                    queue.put_nowait((state_copy, idempotency_key))

        # Now we update state related to idempotency (if any).
        if idempotency_key is not None:
            assert idempotent_mutation is not None
            idempotent_mutations = (
                self._idempotent_mutations
                if transaction is None else transaction.idempotent_mutations
            )
            assert idempotency_key not in idempotent_mutations
            idempotent_mutations[idempotency_key] = idempotent_mutation

    def validate_transaction_participant(
        self,
        context: Context,
        transaction: StateManager.Transaction,
    ):
        """Helper to validate that a transaction participant is conforming to
        the requirements of being a participant."""
        # We *MUST* have persisted the transaction before returning any
        # value back to the caller. Check that this is the case.
        assert transaction._stored, 'Transaction not persisted'

        # All outstanding RPCs must complete before returning (and
        # it should always be > 0 otherwise we have a bug).
        assert context.outstanding_rpcs >= 0, (
            f'context.outstanding_rpcs == {context.outstanding_rpcs}'
        )

        # Check that the tasks of the transaction all belong to the same service
        # as the transaction.
        assert all(
            task.task_id.service == context.service_name
            for task in transaction.tasks
        ), 'Transaction contains tasks not belonging to transaction'

        if context.outstanding_rpcs > 0:
            # TODO(benh): test this case!
            raise RuntimeError(
                'Detected outstanding RPCs; all RPCs must be '
                'await\'ed when performing a transaction'
            )

    @asynccontextmanager
    async def transactionally(
        self,
        context: ReaderContext | WriterContext | TransactionContext,
        tasks_dispatcher: TasksDispatcher,
    ) -> AsyncIterator[Optional[StateManager.Transaction]]:
        """Overload of StateManager.transactionally(...) for
        SidecarStateManager.
        """
        service = context.service_name
        actor_id = context.actor_id

        if context.transaction_id is None:
            yield None
            # Nothing else to do after control is returned to this
            # context manager, just return!
            return

        assert context.transaction_coordinator_service is not None
        assert context.transaction_coordinator_actor_id is not None

        transaction: Optional[StateManager.Transaction] = None

        while True:
            transaction = self._participant_transactions[service].get(actor_id)
            if transaction is None:
                # Add transaction so other transactions will queue.
                transaction = StateManager.Transaction.from_context(
                    context, tasks_dispatcher
                )

                self._participant_transactions[service][actor_id] = transaction

                # Wait for any non-transactional writers!
                await self._mutator_locks[service][actor_id].acquire()

                break
            elif transaction.id != context.transaction_id:
                # Wait for any unfinished transactions! But ignore
                # any raised errors as this isn't our transaction
                # and we want to retry the loop.
                try:
                    await transaction
                except:
                    pass
            elif transaction.finished():
                # TODO(benh): add a test case for this!
                committed_or_aborted = "committed" if transaction.committed(
                ) else "aborted"
                raise RuntimeError(
                    f'Transaction was {committed_or_aborted}; do you have '
                    'a rogue RPC, e.g., from an asynchronous computation '
                    'that you forgot to wait for?'
                )
            elif transaction.prepared():
                # TODO(benh): add a test case for when we find out
                # that a transaction is no longer running due to
                # trying to watch it and yet we still think we are
                # running and instead need to stop running.
                raise RuntimeError(
                    'Transaction has been prepared; do you have a rogue '
                    'RPC, e.g., from an asynchronous computation that '
                    'you forgot to wait for?'
                )
            elif transaction.must_abort:
                # Rather than waste cycles on a transaction that will
                # eventually abort we try and propagate failure sooner.
                #
                # TODO(while-false): Check code path and add test.
                raise RuntimeError('Transaction must abort')
            else:
                break

        assert transaction is not None

        try:
            yield transaction

            # Now that control has resumed here we're exiting the
            # context manager so we can validate the user is following
            # the transaction requirements as well start watching the
            # coordinator for any updates about the transaction.

            self.validate_transaction_participant(context, transaction)
        except:
            # TODO(benh): test this case!
            transaction.must_abort = True
            raise
        finally:
            # TODO(benh): test this case!
            if context.transaction_must_abort:
                transaction.must_abort = True

            # Start watching the transaction.
            #
            # This needs to be done _after_ the servicer method has
            # completed because if we find out via watching that the
            # transaction is committed/aborted we will finish the
            # transaction, remove it from '_participant_transactions'
            # (allowing other transactions to proceed), and release
            # the mutator lock, which can not be done until after the
            # servicer method has completed!
            #
            # NOTE: we CAN NOT preemptively finish the transaction,
            # e.g., to allow other writers or transactions to proceed,
            # because it's possible that this service/actor might be
            # re-involved in the same transaction until the
            # transaction has finished.
            #
            # Also, the watch task may already be started by a
            # different RPC (or by recovery) and we only want one of
            # them!
            #
            # Finally, the transaction may already be completed if the
            # coordinator == participant and two phase commit was
            # successful so we don't need to watch anything.
            if transaction.watch_task is None and not transaction.finished():
                transaction.watch_task = asyncio.create_task(
                    self._transaction_participant_watch(
                        context.channel_manager, transaction
                    )
                )

    @asynccontextmanager
    async def reader(self, context: ReaderContext,
                     state_type: type[Message]) -> AsyncIterator[Message]:
        """Overload of StateManager.reader(...) for SidecarStateManager."""
        # Every reader/writer gets a copy of their own state so
        # that they can execute concurrently.
        #
        # TODO(benh): investigate overriding __delattr__ and
        # __setattr__ such that either we make the states immutable
        # and thus can share them rather than copy them, or we do some
        # kind of copy-on-write.
        state_copy = state_type()
        state_copy.CopyFrom(
            await self._load(context, state_type, from_reader=True)
        )
        yield state_copy

    @asynccontextmanager
    async def streaming_reader(
        self, context: ReaderContext, state_type: type[Message]
    ) -> AsyncIterator[AsyncIterator[Message]]:

        async def iterator() -> AsyncIterator[Message]:
            async with self.streaming_reader_idempotency_key(
                context, state_type
            ) as states:
                async for (state, idempotency_key) in states:
                    yield state

        states = iterator()

        try:
            yield states
        finally:
            # And close the generator proactively so everything can
            # promptly be garbage collected.
            await states.aclose()

    @asynccontextmanager
    async def streaming_reader_idempotency_key(
        self, context: ReaderContext, state_type: type[Message]
    ) -> AsyncIterator[AsyncIterator[Tuple[Message, Optional[uuid.UUID]]]]:
        service = context.service_name
        actor_id = context.actor_id

        transaction: Optional[StateManager.Transaction] = None

        if context.transaction_id is not None:
            transaction = self._participant_transactions[service].get(actor_id)
            assert transaction is not None

        # NOTE: concurrency is a little tricky here! We want to
        # _atomically_ load the state _and_ add our queue so that we
        # don't miss any state updates. We do that by first adding our
        # queue to the list, which we know will not yield the event loop.
        #
        # Next we look to see if we have a cached state, which we can
        # also do without yielding the event loop. If we do have a
        # cached state, then we'll use that as the first state that
        # we'll yield below.
        #
        # If we don't have a cached state then we'll try and load the
        # state and in doing so the loaded state will get enqueued on
        # the queue (see '_load()' for where we do this) since we
        # already added our queue to the list. Of course, it's
        # possible another coroutine will win the loading race before
        # us but then it will enqueue the loaded state on our queue,
        # again, because we already added our queue to the list.

        queue: asyncio.Queue[Optional[Message]] = asyncio.Queue()

        if transaction is None:
            self._streaming_readers[service].setdefault(
                actor_id,
                [],
            ).append(queue)
        else:
            transaction.streaming_readers.append(queue)

        async def iterator(state: Optional[Message]) -> AsyncIterator[Message]:
            # Every reader/writer gets a copy of their own state so
            # that they can execute concurrently.
            #
            # TODO(benh): investigate overriding __delattr__ and
            # __setattr__ such that either we make the states immutable
            # and thus can share them rather than copy them, or we do some
            # kind of copy-on-write.
            state_copy = state_type()

            if state is not None:
                state_copy.CopyFrom(state)
                yield (state_copy, None)

            while True:
                next_state_and_idempotency_key: Optional[Tuple[
                    Message, Optional[uuid.UUID]]] = await queue.get()

                # Currently stream is never "closed" so we should
                # never not have state unless we're in a transaction
                # that was aborted!
                if next_state_and_idempotency_key is None:
                    if transaction is not None:
                        assert transaction.finished()
                        assert not transaction.committed()
                        raise RuntimeError('Transaction aborted!')

                assert next_state_and_idempotency_key is not None

                next_state, idempotency_key = next_state_and_idempotency_key

                # We create _another_ copy of the state _here_ rather
                # than when each time a state is added to a queue so
                # that we don't make unnecessary copies, i.e., we only
                # copy when a reader actually wants the state.
                state_copy.CopyFrom(next_state)
                yield (state_copy, idempotency_key)

        state: Optional[Message] = self._states[service].get(actor_id)

        if state is None:
            await self._load(context, state_type, from_reader=True)

        states = iterator(state)

        try:
            yield states
        finally:
            # Remove our queue from the list so that states aren't
            # added to it anymore.
            if transaction is None:
                self._streaming_readers[service][actor_id].remove(queue)
            else:
                transaction.streaming_readers.remove(queue)

            # And close the generator proactively so everything can
            # promptly be garbage collected.
            await states.aclose()

    @asynccontextmanager
    async def writer(
        self,
        context: WriterContext,
        state_type: type[Message],
        *,
        transaction: Optional[StateManager.Transaction] = None,
        from_constructor: bool = False,
        requires_constructor: bool = False
    ) -> AsyncIterator[Tuple[Message, StateManager.Writer]]:
        """Overload of StateManager.writer(...) for SidecarStateManager."""
        service = context.service_name
        actor_id = context.actor_id
        # To ensure only one writer at a time we use a lock. If we're
        # in a transaction then we should already have acquired the
        # mutator lock but we still need to acquire the "transaction
        # writer lock" so that only one writer will execute at a time
        # within a transaction.
        if transaction is not None:
            assert self._mutator_locks[service][actor_id].locked()

        mutator_or_transaction_writer_lock: asyncio.Lock = (
            self._mutator_locks[service][actor_id] if transaction is None else
            self._transaction_writer_locks[service][actor_id]
        )
        async with mutator_or_transaction_writer_lock:
            # Every reader/writer gets a copy of their own state so
            # that they can execute concurrently.
            state_copy = state_type()
            state_copy.CopyFrom(
                await self._load(
                    context,
                    state_type,
                    from_constructor=from_constructor,
                    requires_constructor=requires_constructor
                )
            )

            async def complete(effects: Effects) -> None:
                if transaction is None:
                    await self._store(
                        service=service,
                        actor_id=actor_id,
                        effects=effects,
                        idempotency_key=context.idempotency_key,
                    )
                else:
                    # NOTE: we do this store while holding the
                    # transaction lock so any outstanding readers
                    # won't also try and store this transaction in the
                    # sidecar as well (instead they'll wait until we
                    # finish storing and then see that we've stored
                    # and just return).
                    async with transaction.lock:
                        await self._store(
                            service=service,
                            actor_id=actor_id,
                            effects=effects,
                            transaction=transaction,
                            idempotency_key=context.idempotency_key,
                        )
                        transaction.stored = True

            yield (state_copy, StateManager.Writer(complete))

    @asynccontextmanager
    async def task_reader(
        self, context: ReaderContext, state_type: type[Message]
    ) -> AsyncIterator[Tuple[Message, StateManager.TaskReader]]:
        """Loads the state for a code generated task reader.
        """
        async with self.reader(context, state_type) as state:

            async def complete(task_effect: TaskEffect, response: Message):
                # Mark this Task as completed in persistent storage.
                # Even though we're writing here, we're not writing the actor's
                # state, and only one instance of this Task will be running at a
                # time, so we don't need to acquire a write lock.
                await self._store(
                    service=task_effect.task_id.service,
                    actor_id=task_effect.task_id.actor_id,
                    completed_task=sidecar_pb2.Task(
                        task_id=task_effect.task_id,
                        method=task_effect.method_name,
                        status=sidecar_pb2.Task.Status.COMPLETED,
                        request=task_effect.request.SerializeToString(),
                        response=response.SerializeToString(),
                    )
                )

            yield (state, StateManager.TaskReader(complete))

    @asynccontextmanager
    async def task_writer(
        self, context: WriterContext, state_type: type[Message]
    ) -> AsyncIterator[Tuple[Message, StateManager.TaskWriter]]:
        """Loads the state for a code generated task writer, e.g., performing
        any necessary functionality to ensure only one writer at a time.
        """
        # Call self.writer to acquire a write lock.
        async with self.writer(context, state_type) as (state, writer):

            async def complete(task_effect: TaskEffect, effects: Effects):
                # We have an invariant here that the returned Effects for each
                # code-generated writer method, including all Task writers, must
                # contain a response that is not None - and that the response is
                # checked in the constructor of each code-generated *Effects
                # class.
                assert effects.response is not None

                # In addition to creating any new tasks, mark this task as
                # completed and store its response.
                completed_task = sidecar_pb2.Task(
                    task_id=task_effect.task_id,
                    method=task_effect.method_name,
                    status=sidecar_pb2.Task.Status.COMPLETED,
                    request=task_effect.request.SerializeToString(),
                    response=effects.response.SerializeToString(),
                )

                # NOTE: not expecting a task writer to ever have an
                # idempotency key and thus no need to pass it to the
                # sidecar. This is because the task either atomically
                # completes itself or not, so we shouldn't ever be
                # retrying a task writer that has updated state in the
                # sidecar because it will have been marked completed.
                assert context.idempotency_key is None

                await self._store(
                    service=task_effect.task_id.service,
                    actor_id=task_effect.task_id.actor_id,
                    effects=effects,
                    completed_task=completed_task,
                )

            yield (state, StateManager.TaskWriter(complete))

    @asynccontextmanager
    async def transaction(
        self,
        context: TransactionContext,
        state_type: type[Message],
        transaction: StateManager.Transaction,
        *,
        from_constructor: bool = False,
        requires_constructor: bool = False
    ) -> AsyncIterator[Callable[[Message], Awaitable[None]]]:
        """Overload of StateManager.transaction(...) for SidecarStateManager."""
        service = context.service_name
        actor_id = context.actor_id

        # At this point we should already be executing
        # "transactionally".
        assert self._participant_transactions[service][actor_id] == transaction

        # We should already hold the mutator lock!
        assert self._mutator_locks[service][actor_id].locked()

        # And we shouldn't have a transaction that must abort, e.g., a
        # transaction that was recovered but not prepared.
        #
        # Specifically in the case of transaction recovery it is
        # important that we don't load and return state that does not
        # actually reflect state that may have been updated as part of
        # the transaction but which we have now lost because we
        # restarted. Instead, we want to fail and propagate that
        # failure as soon as possible.
        assert not transaction.must_abort

        # Need to try and load the state to handle non-constructor
        # transactions for actors that are not yet constructed!
        await self._load(
            context,
            state_type,
            from_constructor=from_constructor,
            requires_constructor=requires_constructor
        )

        # We're starting a new transaction here, so we should have a
        # unique identifier, and it should not already be being
        # tracked as a transaction that we're coordinating.
        assert transaction.id not in self._coordinator_prepared

        # We don't (yet) support nested transactions, so that means we are the
        # coordinator! Check the `context` and the `transaction` to verify this.
        assert not context.nested
        assert (
            (service, actor_id) == (
                transaction.coordinator_service,
                transaction.coordinator_actor_id,
            )
        ), f'{service} {actor_id} is not the transaction coordinator'

        # We need to add the prepared future _before_ we yield control
        # to the servicer so any participants that it calls will be
        # able to start their watch control loops.
        self._coordinator_prepared[transaction.id] = asyncio.Future()

        async def complete(response: Message) -> None:
            # While we don't (yet) have nested transactions, we still
            # need to store the transaction because this method is a
            # transaction participant _in addition_ to being a
            # transaction coordinator, hence like all other
            # participants we need to store the transaction.
            #
            # NOTE: it's possible that we've already stored the
            # transaction, e.g., if we had an inline writer, but we
            # need to try and store the response if we have an
            # idempotency key.
            async with transaction.lock:
                if (
                    not transaction.stored or
                    context.idempotency_key is not None
                ):
                    await self._store(
                        service=service,
                        actor_id=actor_id,
                        transaction=transaction,
                        idempotency_key=context.idempotency_key,
                        response=response,
                    )
                    transaction.stored = True

        try:
            yield complete

            # Always perform two phase commit as the coordinator since we don't
            # yet have nested transactions.

            # Before performing two phase commit we need to perform
            # some validatation just as we do for any method in a
            # transaction (however since we are nested within
            # 'transactionally()' the validation won't be performed
            # there until after the transaction has actually
            # finished, hence, we need to first do it here).
            #
            # In the event validation raises we'll short circuit to
            # the abort phase of two phase commit which will "goto"
            # the `except` block below to actually run the abort.
            self.validate_transaction_participant(context, transaction)

            # If we know our participant will abort this transaction
            # then there is no need to do the prepare phase of two
            # phase commit as it will waste unnecessary cycles (even
            # though it is safe). Instead, we short circuit to the
            # abort phase of two phase commit by raising an error here
            # which will "goto" the `except` block below to actually
            # run the abort.
            if transaction.must_abort:
                raise RuntimeError('Transaction must abort')

            # Two phase commit: (1) prepare
            await self._transaction_coordinator_prepare(
                context.channel_manager, transaction.id, context.participants
            )

            # TODO(benh): if all of the participants were able to
            # prepare successfully consider retrying the sidecar call
            # more than once!
            await self._sidecar_client.transaction_coordinator_prepared(
                transaction.id, context.participants
            )
        except:
            traceback.print_exc()

            # Best effort try and tell the participants that the
            # transaction was aborted; if they don't hear from us now
            # they'll find out when they watch on their own.
            await self._transaction_coordinator_abort(
                context.channel_manager, transaction.id, context.participants
            )

            # Signal that this transaction was unable to be prepared.
            self._coordinator_prepared[transaction.id].set_result(False)

            # Remove transaction so that participants "watch control
            # loop" will determine that the transaction has aborted!
            del self._coordinator_prepared[transaction.id]

            raise
        else:
            # Two phase commit: (2) commit
            #
            # TODO(benh): remove these tasks once they complete!
            self._coordinator_commit_control_loop_tasks[
                transaction.id] = asyncio.create_task(
                    self._transaction_coordinator_commit_control_loop(
                        context.channel_manager,
                        transaction.id,
                        context.participants,
                    )
                )

    def get_response_if_idempotent_mutation(
        self,
        context: WriterContext | TransactionContext,
    ) -> Optional[bytes]:
        """Overload of StateManager.get_response_if_idempotent_mutation(...)
        for SidecarStateManager.
        """
        if context.idempotency_key is None:
            return None

        idempotent_mutations = self._idempotent_mutations

        if context.transaction_id is not None:
            transaction = self._participant_transactions[
                context.service_name].get(context.actor_id)

            if transaction is not None and context.transaction_id == transaction.id:
                # TODO(benh): check if the idempotency key exists in
                # self._idempotent_mutations and if it does raise an
                # error that the user is incorreclty reusing an
                # idempotency key (within a transaction). While we
                # can't check for all incorrect uses, any that we can
                # check for will help the user sort out bugs.
                idempotent_mutations = transaction.idempotent_mutations

        idempotent_mutation = idempotent_mutations.get(context.idempotency_key)

        if idempotent_mutation is not None:
            return idempotent_mutation.response
        else:
            return None

    async def load_task_response(self,
                                 task_id: tasks_pb2.TaskId) -> Optional[bytes]:
        """Loads the response for the given task. Returns None if the task is
        not yet complete. Throws if the task ID is not recognized.
        """
        return await self._sidecar_client.load_task_response(task_id)

    async def read(
        self,
        context: TransactionContext,
        state_type: type[Message],
    ) -> Message:
        """Overload of StateManager.read(...) for SidecarStateManager."""
        return await self._load(context, state_type)

    async def _transaction_coordinator_prepare(
        self,
        channel_manager: _ChannelManager,
        transaction_id: uuid.UUID,
        participants: Participants,
    ):
        """Helper for a transaction coordinator performing the prepare step of
        two phase commit."""
        try:
            # TODO(benh): do in parallel!
            for (service, actor_id) in participants:
                channel = channel_manager.get_channel_from_service_name(
                    service, actor_id
                )

                stub = transactions_pb2_grpc.ParticipantStub(channel)

                await stub.Prepare(
                    transactions_pb2.PrepareRequest(
                        service=service,
                        actor_id=actor_id,
                        transaction_id=transaction_id.bytes
                    )
                )
        except:
            # TODO(benh): handle failed transaction!
            raise

    async def _transaction_coordinator_commit(
        self,
        channel_manager: _ChannelManager,
        transaction_id: uuid.UUID,
        participants: Participants,
    ):
        """Helper for a transaction coordinator performing the commit step of
        two phase commit."""
        for (service, actor_id) in participants:
            # TODO(benh): do in parallel!
            channel = channel_manager.get_channel_from_service_name(
                service, actor_id
            )

            stub = transactions_pb2_grpc.ParticipantStub(channel)

            await stub.Commit(
                transactions_pb2.CommitRequest(
                    service=service,
                    actor_id=actor_id,
                    transaction_id=transaction_id.bytes
                )
            )

    async def _transaction_coordinator_abort(
        self,
        channel_manager: _ChannelManager,
        transaction_id: uuid.UUID,
        participants: Participants,
    ):
        for (service, actor_id) in participants:
            try:
                channel = channel_manager.get_channel_from_service_name(
                    service, actor_id
                )

                stub = transactions_pb2_grpc.ParticipantStub(channel)

                await stub.Abort(
                    transactions_pb2.AbortRequest(
                        service=service,
                        actor_id=actor_id,
                        transaction_id=transaction_id.bytes
                    )
                )
            except:
                # NOTE: aborting is best effort abort, each
                # participant is responsible for checking back in with
                # the coordinator as well in case we were unable to
                # send an abort to them.
                continue

    async def _transaction_participant_watch(
        self,
        channel_manager: _ChannelManager,
        transaction: StateManager.Transaction,
    ):
        # Keep watching the coordinator even in the face of connection
        # failures or coordinator restarts.
        while not transaction.finished():
            try:
                channel = channel_manager.get_channel_from_service_name(
                    transaction.coordinator_service,
                    transaction.coordinator_actor_id,
                )

                stub = transactions_pb2_grpc.CoordinatorStub(channel)

                # TODO(benh): consider doing an 'asyncio.wait()' that
                # also waits for 'transaction' itself so that we stop
                # watching on the coordinator once it reaches out for
                # us to commit/abort.

                watch_response = await stub.Watch(
                    transactions_pb2.WatchRequest(
                        transaction_id=transaction.id.bytes
                    )
                )

                if not watch_response.aborted:
                    await self.transaction_participant_commit(transaction)
                else:
                    await self.transaction_participant_abort(transaction)
                break
            except Exception as e:
                # TODO(benh): print exception if we are verbose logging.
                # traceback.print_exc()

                # Yield the event loop in the event that we'll have an
                # immediate failure again so other things can run
                # before we retry.
                #
                # TODO(benh): do an exponential backoff.
                await asyncio.sleep(0)

    def add_to_server(self, server: grpc.aio.Server) -> None:
        transactions_pb2_grpc.add_CoordinatorServicer_to_server(self, server)
        transactions_pb2_grpc.add_ParticipantServicer_to_server(self, server)

    async def Watch(
        self, request: transactions_pb2.WatchRequest,
        grpc_context: grpc.aio.ServicerContext
    ) -> transactions_pb2.WatchResponse:
        transaction_id = uuid.UUID(bytes=request.transaction_id)
        prepared = self._coordinator_prepared.get(transaction_id)

        # If we don't know about the transaction than treat is as
        # aborted. This is possible, e.g., after a consensus where a
        # coordinator was running gets restarted before finishing a
        # transaction and thus all participants that are trying to
        # watch need to find out that the transaction should be
        # considered aborted.
        if prepared is None:
            return transactions_pb2.WatchResponse(aborted=True)
        else:
            return transactions_pb2.WatchResponse(aborted=not await prepared)

    async def Prepare(
        self, request: transactions_pb2.PrepareRequest,
        grpc_context: grpc.aio.ServicerContext
    ) -> transactions_pb2.PrepareResponse:
        service = request.service
        actor_id = request.actor_id
        transaction_id = uuid.UUID(bytes=request.transaction_id)
        transaction = self._participant_transactions[service].get(actor_id)
        if transaction is None:
            raise RuntimeError(
                f"No pending transaction for service '{service}' "
                f"actor '{actor_id}'"
            )
        elif transaction.id != transaction_id:
            raise RuntimeError('Pending transaction id differs')
        else:
            # All RPCs that are part of this transaction should
            # have completed which means all streaming readers
            # should have completed!
            assert len(transaction.streaming_readers) == 0

            await transaction.tasks_dispatcher.validate(transaction.tasks)

            if transaction.must_abort:
                raise RuntimeError('Transaction must abort')

            # TODO(benh): take advantage of the fact that only
            # prepared transactions can be recovered and instead of
            # storing state in the sidecar after each write, instead
            # store the state in memory and pass the updated state and
            # tasks to the sidecar here.

            await self._sidecar_client.transaction_participant_prepare(
                service, actor_id
            )

            transaction.prepare()

            return transactions_pb2.PrepareResponse()

    async def Commit(
        self, request: transactions_pb2.CommitRequest,
        grpc_context: grpc.aio.ServicerContext
    ) -> transactions_pb2.CommitResponse:
        service = request.service
        actor_id = request.actor_id
        transaction_id = uuid.UUID(bytes=request.transaction_id)
        transaction = self._participant_transactions[service].get(actor_id)

        # It's possible the transaction was already committed from
        # watching, and we might even be on to another transaction, so
        # we can let the coordinator know we are all set.
        if transaction is None or transaction.id != transaction_id:
            return transactions_pb2.CommitResponse()

        await self.transaction_participant_commit(transaction)

        # NOTE: we don't bother cancelling 'transaction.watch_task'
        # because it will complete on it's own once it notices that
        # the transaction has finished (either when it retries to
        # watch or when it hears back from the coordinator).
        #
        # Also, a watch task doesn't start until after control is
        # exited from 'transactionally()', which means that we might
        # not have started a watch task if the coordinator ==
        # participant since we may be in the middle of two phase
        # commit.
        #
        # We might we want to try and preemptively cancel the task to
        # lessen the strain on the coordinator but this appears more
        # difficult than just doing 'transaction.watch_task.cancel()'
        # as it looks like that propagates cancellation in unexpected
        # ways.

        return transactions_pb2.CommitResponse()

    async def Abort(
        self, request: transactions_pb2.AbortRequest,
        grpc_context: grpc.aio.ServicerContext
    ) -> transactions_pb2.AbortResponse:
        service = request.service
        actor_id = request.actor_id
        transaction_id = uuid.UUID(bytes=request.transaction_id)
        transaction = self._participant_transactions[service].get(actor_id)

        # It's possible the transaction was already aborted from
        # watching, and we might even be on to another transaction, so
        # we can let the coordinator know we are all set.
        if transaction is None or transaction.id != transaction_id:
            return transactions_pb2.AbortResponse()

        await self.transaction_participant_abort(transaction)

        # NOTE: we don't bother cancelling 'transaction.watch_task'
        # because it will complete on it's own once it notices that
        # the transaction has finished (either when it retries to
        # watch or when it hears back from the coordinator).
        #
        # Also, a watch task doesn't start until after control is
        # exited from 'transactionally()', which means that we might
        # not have started a watch task if the coordinator ==
        # participant since we may be in the middle of two phase
        # commit.
        #
        # We might we want to try and preemptively cancel the task to
        # lessen the strain on the coordinator but this appears more
        # difficult than just doing 'transaction.watch_task.cancel()'
        # as it looks like that propagates cancellation in unexpected
        # ways.

        return transactions_pb2.AbortResponse()

    async def transaction_participant_store(
        self, transaction: StateManager.Transaction
    ):
        # NOTE: doing double checked locking here so that we don't block if
        # there is a concurrent writer doing a store which it always does while
        # holding the transaction lock even though the transaction might already
        # be stored (e.g., by an earlier reader or writer). For this, we use
        # `_stored` to "unsafely" peek at the value.
        if not transaction._stored:
            async with transaction.lock:
                if not transaction.stored:
                    await self._store(
                        service=transaction.service,
                        actor_id=transaction.actor_id,
                        transaction=transaction,
                    )
                    transaction.stored = True

    async def transaction_participant_commit(
        self, transaction: StateManager.Transaction
    ):
        service = transaction.service
        actor_id = transaction.actor_id

        # NOTE: there is a possible race where either the watch will
        # try and commit or the coordinator will reach out to the
        # participant to commit hence the need to lock as well as
        # check if the transaction has finished.
        async with transaction.lock:
            if not transaction.finished():
                # TODO(benh): add test case for sidecar failure!
                await self._sidecar_client.transaction_participant_commit(
                    service, actor_id
                )

                # NOTE: invariant here is everything after this line
                # SHOULD NOT RAISE!
                #
                # If we raise while calling the sidecar above then
                # we'll retry, either via the watch or via the
                # coordinator (who ever ultimately called this
                # method).
                #
                # After this comment nothing can be retried again so
                # it SHOULD NOT RAISE.

                self._states[service][actor_id] = transaction.state

                queues = self._streaming_readers[service].get(actor_id)

                if queues is not None:
                    for queue in queues:
                        # NOTE: we defer making a reader specific copy
                        # of this state until the reader actually
                        # reads it to reduce memory usage.
                        queue.put_nowait(
                            (transaction.state, transaction.idempotency_key)
                        )

                # NOTE: while dispatching tasks is idempotent and can
                # be "retried" if necessary, the tasks should not run
                # until after the state has been updated since they
                # may rely on that state!
                if len(transaction.tasks) > 0:
                    transaction.tasks_dispatcher.dispatch(transaction.tasks)

                # Add all idempotent mutations that occurred within
                # this transaction.
                #
                # TODO(benh): once the transaction is committed the
                # idempotency keys used for mutations within the
                # transaction are really only useful for detecting when
                # a user has incorrectly reused an idempotency key. We
                # don't do any of those checks now, and in the future
                # we might explicitly decide _not_ to store
                # idempotency keys within a transaction to improve
                # performance (or possibly make it configurable so
                # users can tradeoff performance for better error
                # detection of their own code).
                self._idempotent_mutations.update(
                    transaction.idempotent_mutations
                )

                transaction.commit()

                self._participant_transactions[service].pop(actor_id)

                assert self._mutator_locks[service][actor_id].locked()
                self._mutator_locks[service][actor_id].release()

    async def transaction_participant_abort(
        self, transaction: StateManager.Transaction
    ):
        service = transaction.service
        actor_id = transaction.actor_id

        # NOTE: there is a possible race where either the watch will
        # try and commit or the coordinator will reach out to the
        # participant to commit hence the need to lock as well as
        # check if the transaction has finished.
        async with transaction.lock:
            if not transaction.finished():

                # We only reach out to the sidecar to abort in case we have
                # persisted anything.
                if transaction.stored:
                    # TODO(benh): add test case for sidecar failure!
                    await self._sidecar_client.transaction_participant_abort(
                        service, actor_id
                    )

                # NOTE: invariant here is everything after this line
                # SHOULD NOT RAISE!
                #
                # If we raise while calling the sidecar above then
                # we'll retry, either via the watch or via the
                # coordinator (who ever ultimately called this
                # method).
                #
                # After this comment nothing can be retried again so
                # it SHOULD NOT RAISE.

                # Need to abort all streaming readers that are part of
                # this transaction!
                for queue in transaction.streaming_readers:
                    queue.put_nowait(None)

                transaction.abort()

                self._participant_transactions[service].pop(actor_id)

                assert self._mutator_locks[service][actor_id].locked()
                self._mutator_locks[service][actor_id].release()

    async def recover(
        self,
        channel_manager: _ChannelManager,
        middleware_by_service_name: dict[ServiceName, Middleware],
        file_descriptor_set: FileDescriptorSet,
    ) -> None:
        """Attempt to recover server state after a potential restart."""
        recover_response = await self._sidecar_client.recover()

        # If there is a recovered file descriptor set, check for backwards
        # compatibility.
        if recover_response.HasField('file_descriptor_set'):
            validate_descriptor_sets_are_backwards_compatible(
                recover_response.file_descriptor_set,
                file_descriptor_set,
            )
        # We've passed any backwards compatibility checks, so we're safe to
        # overwrite the old file descriptor set with the new one.
        await self._sidecar_client.store(
            actor_upserts=[],
            task_upserts=[],
            file_descriptor_set=file_descriptor_set,
        )

        # Need to declare this up here as it is used in multiple scopes.
        middleware: Optional[Middleware] = None

        # To avoid dispatching only some tasks in case of a RuntimeError thrown
        # below, we save all the tasks here alongside their matching middleware
        # and dispatch them only after recovering everything.
        task_effects_by_middleware: defaultdict[
            Middleware, list[TaskEffect]] = defaultdict(list)

        for task in recover_response.pending_tasks:
            # Find the correct servicer middleware to handle this task, and use
            # it to recover the task's dispatch information.
            middleware = middleware_by_service_name.get(task.task_id.service)

            if middleware is None:
                # TODO(#1443): Clean up this error handling once we have
                # validation of service backwards compatibility for in-use task
                # methods.
                raise RuntimeError(
                    f"Missing middleware for service '{task.task_id.service}' "
                    f"when restarting task '{task.task_id}'"
                )

            if task.method not in middleware.request_type_by_method_name:
                # TODO(#1443): Clean up this error handling once we have
                # validation of service backwards compatibility for in-use task
                # methods.
                raise RuntimeError(
                    f"Task method '{task.method}' has no registered "
                    f"request type in middleware. Was the method removed?"
                )

            try:
                task_effect = TaskEffect.from_sidecar_task(
                    task,
                    middleware.request_type_by_method_name[task.method],
                )
            except Exception as e:
                # TODO(#1443): Clean up this error handling once we have
                # validation of service backwards compatibility for in-use task
                # methods.
                raise RuntimeError(f'Error parsing task request') from e
            else:
                task_effects_by_middleware[middleware].append(task_effect)

        # All tasks recovered, let's dispatch them.
        for middleware, task_effects in task_effects_by_middleware.items():
            middleware.tasks_dispatcher.dispatch(task_effects)

        # Now recover any ongoing transactions.
        for sidecar_transaction in recover_response.participant_transactions:
            middleware = middleware_by_service_name.get(
                sidecar_transaction.service
            )

            if middleware is None:
                # TODO(#1443): Clean up this error handling once we have
                # validation of service backwards compatibility.
                raise RuntimeError(
                    f"Missing middleware for service '{task.task_id.service}' "
                    "when recovering transaction "
                    f"'{str(uuid.UUID(sidecar_transaction.transaction_id))}'"
                )

            transaction = StateManager.Transaction.from_sidecar(
                sidecar_transaction, middleware
            )

            # This transaction should NOT already be recovered!
            assert transaction.actor_id not in self._participant_transactions[
                transaction.service]

            self._participant_transactions[transaction.service][
                transaction.actor_id] = transaction

            # The mutator lock should not be held yet as recovery
            # _must_ occur before we start serving and as we asserted
            # above there are not multiple transactions per actor!
            assert not self._mutator_locks[transaction.service][
                transaction.actor_id].locked()

            await self._mutator_locks[transaction.service][transaction.actor_id
                                                          ].acquire()

            # TODO(benh): don't just "watch" the transaction, also
            # proactively tell the coordinator if this transaction
            # 'must_abort' if we recovered an unprepared transaction
            # so that we can abort a long-running transaction sooner
            # rather than later.

            transaction.watch_task = asyncio.create_task(
                self._transaction_participant_watch(
                    channel_manager, transaction
                )
            )

        for (transaction_id, participants) in [
            (uuid.UUID(transaction_id), participants)
            for (transaction_id, participants
                ) in recover_response.prepared_coordinator_transactions.items()
        ]:
            prepared: asyncio.Future[bool] = asyncio.Future()
            prepared.set_result(True)
            self._coordinator_prepared[transaction_id] = prepared

            self._coordinator_commit_control_loop_tasks[
                transaction_id] = asyncio.create_task(
                    self._transaction_coordinator_commit_control_loop(
                        channel_manager,
                        transaction_id,
                        Participants.from_sidecar(participants),
                    )
                )

        for idempotent_mutation in recover_response.idempotent_mutations:
            idempotency_key = uuid.UUID(bytes=idempotent_mutation.key)
            assert idempotency_key not in self._idempotent_mutations
            self._idempotent_mutations[idempotency_key] = idempotent_mutation

    async def _transaction_coordinator_commit_control_loop(
        self,
        channel_manager: _ChannelManager,
        transaction_id: uuid.UUID,
        participants: Participants,
    ) -> None:
        while True:
            try:
                await self._transaction_coordinator_commit(
                    channel_manager, transaction_id, participants
                )

                # We can safely delete the transaction because all
                # participants have acknowledged the commit!
                #
                # NOTE: as of the writing of this comment it is still
                # possible that one of the participants might have
                # started a watch which after we delete the entry from
                # 'self._coordinator_prepared' below would cause
                # that watch to think that the transaction was aborted
                # but when the watch loop actually tries to do the
                # abort it will see that the transaction has actually
                # been finished because a commit was done first (from
                # the call above).
                del self._coordinator_prepared[transaction_id]

                # TODO(benh): garbage collect the transaction prepared
                # entry from the sidecar!

                break
            except:
                # Yield the event loop in the event that we'll have an
                # immediate failure again so other things can run
                # before we retry.
                #
                # TODO(while-false): Log the error. Optionally the stack trace
                # too to help with debugging.
                # TODO(benh): do an exponential backoff.
                await asyncio.sleep(0)

        # Our commit control loop `asyncio.Task` is about to complete. Remove it
        # from the list of active tasks. Note that this has to be done here,
        # since (by design) there may not be anybody else `await`ing the
        # completion of this task.
        del self._coordinator_commit_control_loop_tasks[transaction_id]


class LocalSidecarStateManager(SidecarStateManager):
    """Implementation of state manager that also encapsulates a
    'SidecarServer' for local use.
    """

    def __init__(self, directory: str):
        self._sidecar = SidecarServer(directory)

        # Now call our super constructor with the sidecar address.
        super().__init__(sidecar_address=self._sidecar.address)

    def shutdown(self):
        self._sidecar.shutdown()

    def wait(self):
        self._sidecar.wait()


class NopStateManager(StateManager):
    """Nop implementation of state manager that is a placeholder while we
    are still developing alpha.

    *** THIS SHOULD BE REMOVED ONCE WE HAVE COMPLETED K8S SIDECAR. ***
    """

    @asynccontextmanager
    async def reader(self, context: ReaderContext,
                     state_type: type[Message]) -> AsyncIterator[Message]:
        yield state_type()

    @asynccontextmanager
    async def writer(
        self,
        context: WriterContext,
        state_type: type[Message],
        *,
        transaction: Optional[StateManager.Transaction] = None,
        from_constructor: bool = False,
        requires_constructor: bool = False
    ) -> AsyncIterator[Tuple[Message, StateManager.Writer]]:

        async def complete(effects: Effects) -> None:
            pass

        yield (state_type(), StateManager.Writer(complete))

    def add_to_server(self, server: grpc.aio.Server) -> None:
        pass

    async def recover(
        self,
        channel_manager: _ChannelManager,
        middleware_by_service_name: dict[ServiceName, Middleware],
        file_descriptor_set: FileDescriptorSet,
    ) -> None:
        pass

    @asynccontextmanager
    async def transactionally(
        self,
        context: ReaderContext | WriterContext | TransactionContext,
        tasks_dispatcher: TasksDispatcher,
    ) -> AsyncIterator[Optional[StateManager.Transaction]]:
        """Overload of StateManager.transactionally(...) for
        NopStateManager.
        """
        # The NopStateManager will never persist anything, so there's no point
        # in managing a transaction.
        yield None
        return

    def get_response_if_idempotent_mutation(
        self,
        context: WriterContext | TransactionContext,
    ) -> Optional[bytes]:
        """Overload of StateManager.get_response_if_idempotent_mutation(...)
        for NopStateManager.
        """
        return None
