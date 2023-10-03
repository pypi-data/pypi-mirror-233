from abc import ABC, abstractmethod

from boto3 import client as aws_client
from core.di.injector import Injector


class IMsqManager(ABC):

    @abstractmethod
    def send_msg(self, url: str, payload: str) -> dict:
        raise NotImplementedError()


dependency = Injector()


@dependency.inject()
class MsqManager(IMsqManager):

    def __init__(self):
        super().__init__()
        self._client = aws_client("sqs")

    def send_msg(self, url: str, payload: str) -> dict:
        return self._client.send_message(QueueUrl=url, MessageBody=payload)
