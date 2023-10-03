from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import loads

from boto3 import resource, client
from core.di.injector import Injector


@dataclass
class StorageOptions:
    bucket: str


class IFileStorageManager(ABC):

    @abstractmethod
    def read_json_file(self, name: str) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def add_file(self, name: str, content: any, content_type: str = None):
        raise NotImplementedError()

    @abstractmethod
    def get_latest_file(self, prefix: str) -> str | None:
        raise NotImplementedError()


dependency = Injector()


@dependency.inject()
class FileStorageManager(IFileStorageManager):

    def __init__(self, options: StorageOptions):
        super().__init__()
        self._bucket_name = options.bucket
        self._client = client("s3")
        self._bucket = resource("s3").Bucket(options.bucket)

    def read_json_file(self, name: str) -> dict:
        response = self._client.get_object(Bucket=self._bucket_name, Key=name)
        content = response["Body"].read().decode("utf-8")
        return loads(content)

    def add_file(self, name: str, content: any, content_type: str = ""):
        self._client.put_object(Bucket=self._bucket_name, Key=name, Body=content, ContentType=content_type)

    def get_latest_file(self, prefix: str) -> str | None:
        files = sorted(self._bucket.objects.filter(Prefix=prefix), key=lambda obj: obj.last_modified)
        return files[-1].key if len(files) > 0 else None
