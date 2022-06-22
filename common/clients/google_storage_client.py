from abc import abstractmethod
import logging
import os.path
import shutil

from google.cloud import storage

from common.config import settings
from common.customized_logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class BaseStorageClient:
    def __init__(self, bucket_name_or_directory):
        self.bucket_name_or_directory = bucket_name_or_directory

    @abstractmethod
    def upload(
        self, source_file_full_path, destination_filename, enable_public=False
    ):
        pass

    @abstractmethod
    def list_objects(self, prefix=None):
        pass

    @abstractmethod
    def download(self, source_filename, destination):
        pass


class LocalStorageClient(BaseStorageClient):
    def upload(
        self, source_file_full_path, destination_filename, enable_public=False
    ):

        full_dest_path = os.path.join(
            self.bucket_name_or_directory, destination_filename
        )

        os.path.dirname(full_dest_path)

        "bucket_name_or_directory/style/figures/a.txt"
        "bucket_name_or_directory/asdfas.txt"

        if os.path.isfile(source_file_full_path):
            shutil.copyfile(source_file_full_path, destination_filename)
        elif os.path.isdir(source_file_full_path):
            shutil.copy(source_file_full_path, destination_filename)
        else:
            raise ValueError(f"{destination_filename} does not exist!")

    def download(self, source_filename, destination):
        return source_filename


class MockStorageClient(BaseStorageClient):
    def upload(
        self, source_file_full_path, destination_filename, enable_public=False
    ):
        return destination_filename


class GoogleStorageClient(BaseStorageClient):
    def __init__(self, bucket_name_or_directory):
        super().__init__(bucket_name_or_directory)
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name_or_directory)

    def upload(
        self, source_file_full_path, destination_filename, enable_public=False
    ):
        blob = self.bucket.blob(destination_filename)
        blob.upload_from_filename(source_file_full_path)
        if enable_public:
            blob.make_public()
            return blob.public_url

        return blob.path

    def download(self, source_filename, destination):
        blob = self.bucket.blob(source_filename)
        if isinstance(destination, str):
            full_path = os.path.join(destination, source_filename)
            blob.download_to_filename(full_path)
            return full_path
        else:
            blob.download_to_file(destination)
            return destination.name

    def list_objects(self, prefix=None):
        return self.client.list_blobs(
            self.bucket_name_or_directory, prefix=prefix
        )


def get_storage_client(bucket_name_or_directory):
    """
    If the machine is on GCP, returns GoogleStorageClient, otherwise, returns
    MockStorageClient.
    """

    if settings.ENVIRONMENT == "local":
        return LocalStorageClient(bucket_name_or_directory)

    elif settings.ENVIRONMENT == "test":
        return MockStorageClient(bucket_name_or_directory)

    return GoogleStorageClient(bucket_name_or_directory)
