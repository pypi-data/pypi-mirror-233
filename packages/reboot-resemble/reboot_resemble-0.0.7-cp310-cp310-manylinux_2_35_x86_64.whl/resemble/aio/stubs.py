import grpc_status._async as rpc_status
import uuid
from contextlib import asynccontextmanager
from google.protobuf.message import Message
from grpc.aio import AioRpcError
from resemble.aio.contexts import Context, Participants
from resemble.aio.errors import Aborted
from resemble.aio.headers import IDEMPOTENCY_KEY_HEADER, Headers
from resemble.aio.idempotency import IdempotencyManager
from resemble.aio.internals.channel_manager import _ChannelManager
from resemble.aio.types import ActorId, GrpcMetadata, ServiceName
from typing import AsyncIterator, Callable, Optional, TypeVar

CallT = TypeVar('CallT')


class Stub:
    """Common base class for generated resemble stubs.
    """
    # TODO: Do we add injection for channels and/or interceptors for M1?
    _channel_manager: _ChannelManager
    _headers: Headers

    _idempotency_manager: IdempotencyManager

    # Context that was used to create this stub.
    _context: Optional[Context]

    def __init__(
        self,
        *,
        channel_manager: _ChannelManager,
        idempotency_manager: IdempotencyManager,
        service_name: ServiceName,
        actor_id: ActorId,
        context: Optional[Context],
    ):
        self._channel_manager = channel_manager
        self._idempotency_manager = idempotency_manager
        self._context = context

        transaction_id: Optional[uuid.UUID] = None
        transaction_coordinator_service: Optional[str] = None
        transaction_coordinator_actor_id: Optional[str] = None

        if context is not None:
            transaction_id = context.transaction_id
            transaction_coordinator_service = context.transaction_coordinator_service
            transaction_coordinator_actor_id = context.transaction_coordinator_actor_id

        self._headers = Headers(
            service_name=service_name,
            actor_id=actor_id,
            transaction_id=transaction_id,
            transaction_coordinator_service=transaction_coordinator_service,
            transaction_coordinator_actor_id=transaction_coordinator_actor_id,
        )

    def _grpc_metadata(self) -> GrpcMetadata:
        return self._headers.to_grpc_metadata()

    @asynccontextmanager
    async def _call(
        self,
        method: Callable[..., CallT],
        request_or_requests: Message | AsyncIterator[Message],
        *,
        idempotency_key: Optional[str] = None,
        metadata: Optional[GrpcMetadata] = None,
        error_type: Optional[type[Aborted]] = None,
    ) -> AsyncIterator[CallT]:
        """Helper for making an RPC and properly tracking it if it is part of
        a transaction.
        """
        if metadata is None:
            metadata = ()

        metadata += self._grpc_metadata()

        # TODO(benh): maybe just overwrite the idempotency key instead
        # of checking for its existence?
        if any(t[0] == IDEMPOTENCY_KEY_HEADER for t in metadata):
            raise ValueError(
                f"Do not set '{IDEMPOTENCY_KEY_HEADER}' metadata yourself"
            )

        if idempotency_key is not None:
            metadata += ((IDEMPOTENCY_KEY_HEADER, idempotency_key),)

        if self._context is not None and self._context.transaction_id is not None:
            self._context.outstanding_rpcs += 1

        try:
            call = method(request_or_requests, metadata=metadata)
            yield call
            if self._context is not None and self._context.transaction_id is not None:
                participants = Participants.from_grpc_metadata(
                    await call.trailing_metadata()
                )
                self._context.participants.union(participants)
        except BaseException as exception:
            if self._context is not None and self._context.transaction_id is not None:
                # TODO(benh): considering stringifying the exception
                # to include in the error we raise when doing the
                # prepare stage of two phase commit.
                self._context.transaction_must_abort = True

            if error_type is not None and isinstance(exception, AioRpcError):
                status = await rpc_status.from_call(call)
                if status is not None:
                    error = error_type.from_status(status)
                    if error is not None:
                        raise error

            raise
        finally:
            if self._context is not None and self._context.transaction_id is not None:
                self._context.outstanding_rpcs -= 1
