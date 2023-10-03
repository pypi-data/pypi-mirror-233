"""Utilities for the network module."""
from concurrent import futures

from grpc import Server, server
from typing_extensions import Self

from .arp_pb2_grpc import AIMServicer, add_AIMServicer_to_server


class ServerBuilder:
    """Builder for the server."""

    _server: Server

    def __init__(self) -> None:
        self._server = server(futures.ThreadPoolExecutor(max_workers=8))

    def set_port(self, port: int | str = 50051) -> Self:
        """Set the port of the server.

        Parameters
        ----------
        port : int | str, optional
            the port of the server, by default 50051

        """
        self._server.add_insecure_port(f"[::]:{port}")
        return self

    def add_servicer(self, servicer: AIMServicer) -> Self:
        """Add a servicer to the server.

        A servicer is a class that implements the AIMServicer interface.

        See Also
        --------
        AIMServicer

        """
        add_AIMServicer_to_server(servicer, self._server)
        return self

    def build(self) -> Server:
        """Get the built server."""
        return self._server

    def new(self) -> Self:
        """Reset the builder to its initial state."""
        return ServerBuilder()
