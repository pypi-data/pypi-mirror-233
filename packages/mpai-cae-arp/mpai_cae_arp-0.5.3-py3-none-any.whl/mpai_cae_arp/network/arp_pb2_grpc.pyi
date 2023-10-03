from abc import abstractmethod

from grpc import Channel, Server

from .arp_pb2 import InfoRequest, InfoResponse, JobRequest, JobResponse

class AIMStub:
    def __init__(self, channel: Channel) -> None: ...

class AIMServicer:
    @abstractmethod
    def getInfo(self, request: InfoRequest, context) -> InfoResponse: ...
    @abstractmethod
    def work(self, request: JobRequest, context) -> JobResponse: ...

class AIM:
    @staticmethod
    def getInfo(
        request: InfoRequest,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure: bool = False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ) -> InfoResponse: ...
    @staticmethod
    def work(
        request: JobRequest,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure: bool = False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ) -> JobResponse: ...

def add_AIMServicer_to_server(servicer: AIMServicer, server: Server) -> None: ...
