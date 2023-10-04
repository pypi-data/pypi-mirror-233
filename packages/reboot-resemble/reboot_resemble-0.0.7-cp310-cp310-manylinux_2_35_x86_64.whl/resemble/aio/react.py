import asyncio
import grpc
import traceback
from resemble.aio.headers import Headers
from resemble.aio.internals.middleware import Middleware
from resemble.aio.types import ServiceName
from resemble.v1alpha1 import react_pb2, react_pb2_grpc
from typing import AsyncIterable, Optional


class ReactServicer(react_pb2_grpc.ReactServicer):
    """System service for serving requests from our code generated react
    readers.

    TODO(benh): make this more generic than just for react so that
    users and other system services (e.g., a read cache) can use this
    to get reactive/streaming reads without the user having to
    implement it themselves.
    """

    def __init__(
        self, middleware_by_service_name: dict[ServiceName, Middleware]
    ):
        self._middleware_by_service_name = middleware_by_service_name

    def add_to_server(self, server: grpc.aio.Server) -> None:
        react_pb2_grpc.add_ReactServicer_to_server(self, server)

    async def Query(
        self, request: react_pb2.QueryRequest,
        grpc_context: grpc.aio.ServicerContext
    ) -> AsyncIterable[react_pb2.QueryResponse]:
        """Implements the React.Query RPC that calls into the
        'Middleware.react' method for handling the request."""
        try:
            headers = Headers.from_grpc_context(grpc_context)

            middleware: Optional[Middleware
                                ] = self._middleware_by_service_name.get(
                                    headers.service_name
                                )

            if middleware is None:
                raise ValueError(f"Unknown service '{headers.service_name}'")

            async for (response, idempotency_keys) in middleware.react(
                headers.actor_id, request.method, request.request
            ):
                yield react_pb2.QueryResponse(
                    response=response.SerializeToString(),
                    idempotency_keys=[
                        str(idempotency_key)
                        for idempotency_key in idempotency_keys
                    ],
                )
        except asyncio.CancelledError:
            # It's pretty normal for a query to be cancelled; it's not useful to
            # print a stack trace.
            raise
        except:
            traceback.print_exc()
            raise
