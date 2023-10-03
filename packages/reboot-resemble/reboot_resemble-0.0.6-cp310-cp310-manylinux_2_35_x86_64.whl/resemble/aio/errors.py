from google.protobuf.message import Message


class Aborted(Exception):
    """Base class of all RPC specific code generated errors used for
    aborting an RPC."""

    def __init__(self, *, message: str, detail: Message):
        self.message = message
        self.detail = detail
