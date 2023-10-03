import grpc.aio
import json
import uuid
from collections import defaultdict
from resemble.aio.headers import TRANSACTION_PARTICIPANTS_HEADER, Headers
from resemble.aio.idempotency import IdempotencyManager
from resemble.aio.internals.channel_manager import (
    LegacyGrpcChannel,
    _ChannelManager,
)
from resemble.aio.internals.contextvars import Servicing, _servicing
from resemble.aio.types import ActorId, GrpcMetadata, ServiceName
from resemble.v1alpha1 import sidecar_pb2
from typing import Iterable, Iterator, Optional, Tuple, TypeVar

ContextT = TypeVar('ContextT', bound='Context')


class Participants:
    _participants: defaultdict[ServiceName, set[ActorId]]

    @classmethod
    def from_sidecar(cls, participants: sidecar_pb2.Participants):
        """Constructs an instance from the sidecar protobuf representation."""
        result = cls()
        for (service, actor_ids) in participants.participants.items():
            result.update(service, actor_ids.actor_ids)
        return result

    def to_sidecar(self) -> sidecar_pb2.Participants:
        """Helper to construct the sidecar protobuf representation."""
        return sidecar_pb2.Participants(
            participants={
                service:
                    sidecar_pb2.Participants.ActorIds(
                        actor_ids=list(actor_ids)
                    ) for (service, actor_ids) in self._participants.items()
            },
        )

    def __init__(self):
        self._participants = defaultdict(set)

    def __iter__(self) -> Iterator[Tuple[ServiceName, ActorId]]:
        """Returns an iterator of (service, actor_id) tuples for each
        participant."""
        for service, actor_ids in self._participants.items():
            for actor_id in actor_ids:
                yield (service, actor_id)

    def add(self, service_name: ServiceName, actor_id: ActorId):
        self._participants[service_name].add(actor_id)

    def update(self, service_name: ServiceName, actor_ids: Iterable[ActorId]):
        self._participants[service_name].update(actor_ids)

    def union(self, participants: 'Participants'):
        for (service_name, actor_ids) in participants._participants.items():
            self._participants[service_name].update(actor_ids)

    def to_grpc_metadata(self) -> GrpcMetadata:
        """Helper to encode transaction participants into gRPC metadata.
        """
        return (
            (
                TRANSACTION_PARTICIPANTS_HEADER,
                json.dumps(
                    # Need to convert 'set' into a 'list' for JSON
                    # stringification.
                    {
                        service_name: list(actor_ids)
                        for (service_name,
                             actor_ids) in self._participants.items()
                    }
                )
            ),
        )

    @classmethod
    def from_grpc_metadata(cls, metadata: GrpcMetadata) -> 'Participants':
        """Helper to decode transaction participants from gRPC metadata.
        """
        for (key, value) in metadata:
            if key == TRANSACTION_PARTICIPANTS_HEADER:
                participants = cls()
                for (service_name, actor_ids) in json.loads(value).items():
                    participants.update(service_name, actor_ids)

                return participants

        return cls()


class Context(IdempotencyManager):
    """Common base class for all contexts.

    Contexts holds information relevant to the current call.

    Construction of a Context object is done by the servicer
    middleware. You should never need to construct a Context yourself.
    """
    _channel_manager: _ChannelManager
    _headers: Headers

    # Participants aggregated from all RPCs rooted at the method for
    # which we initially created this context.
    #
    # We use this when a method is executed within a transaction so
    # that we can pass back to the coordinator the precise set of
    # participants.
    participants: Participants

    # Number of outstanding RPCs rooted at the method for which we
    # initially created this context. Incremented whenever an RPC
    # begins, and decremented when it completes (whether successfully
    # or not).
    #
    # We use this when a method is executed within a transaction to
    # ensure that all RPCs complete so that we know we have aggregated
    # all possible participants - this count must reach 0.
    #
    # TODO(benh): consider using this for not just transactions but
    # all methods, or at least making it the default with an option to
    # opt out.
    outstanding_rpcs: int

    # Whether or not the transaction enclosing this context should
    # abort.
    transaction_must_abort: bool

    def __init__(
        self,
        *,
        channel_manager: _ChannelManager,
        headers: Headers,
    ):
        # Note: this is intended as a private constructor only to be
        # called by the middleware.
        if _servicing.get() is not Servicing.INITIALIZING:
            raise RuntimeError(
                'Context should only be constructed by middleware'
            )

        super().__init__()

        self._channel_manager = channel_manager
        self._headers = headers

        self.participants = Participants()
        self.outstanding_rpcs = 0
        self.transaction_must_abort = False

    @property
    def channel_manager(self) -> _ChannelManager:
        """Return channel manager.
        """
        return self._channel_manager

    @property
    def service_name(self) -> ServiceName:
        """Return service name.
        """
        return self._headers.service_name

    @property
    def actor_id(self) -> ActorId:
        """Return actor id.
        """
        return self._headers.actor_id

    @property
    def transaction_id(self) -> Optional[uuid.UUID]:
        """Return transaction id.
        """
        return self._headers.transaction_id

    @property
    def transaction_coordinator_service(self) -> Optional[str]:
        """Return transaction coordinator service.
        """
        return self._headers.transaction_coordinator_service

    @property
    def transaction_coordinator_actor_id(self) -> Optional[str]:
        """Return transaction coordinator actor id.
        """
        return self._headers.transaction_coordinator_actor_id

    @property
    def idempotency_key(self) -> Optional[uuid.UUID]:
        """Return optional idempotency key.
        """
        return self._headers.idempotency_key

    def legacy_grpc_channel(self) -> grpc.aio.Channel:
        """Get a gRPC channel that can connect to any Resemble-hosted legacy
        gRPC service. Simply use this channel to create a Stub and call it, no
        address required."""
        return LegacyGrpcChannel(self._channel_manager)


class ReaderContext(Context):
    """Call context for a reader call."""
    pass


class WriterContext(Context):
    """Call context for a writer call."""
    pass


class TransactionContext(Context):
    """Call context for a transaction call."""

    def __init__(
        self,
        *,
        channel_manager: _ChannelManager,
        headers: Headers,
    ):
        # NOTE: we don't (yet) support nested transactions.
        self._nested = False

        assert headers.transaction_id is None
        assert headers.transaction_coordinator_service is None
        assert headers.transaction_coordinator_actor_id is None

        headers.transaction_id = uuid.uuid4()

        # The actor servicing the request to executing a method of
        # kind transaction acts as the transaction coordinator.
        headers.transaction_coordinator_service = headers.service_name
        headers.transaction_coordinator_actor_id = headers.actor_id

        super().__init__(
            channel_manager=channel_manager,
            headers=headers,
        )

    @property
    def transaction_id(self) -> uuid.UUID:
        """Return transaction id.
        """
        assert self._headers.transaction_id is not None
        return self._headers.transaction_id

    @property
    def transaction_coordinator_service(self) -> str:
        """Return transaction coordinator service.
        """
        assert self._headers.transaction_coordinator_service is not None
        return self._headers.transaction_coordinator_service

    @property
    def transaction_coordinator_actor_id(self) -> str:
        """Return transaction coordinator actor id.
        """
        assert self._headers.transaction_coordinator_actor_id is not None
        return self._headers.transaction_coordinator_actor_id

    @property
    def nested(self) -> bool:
        """Return whether or not this transaction is nested.
        """
        return self._nested
