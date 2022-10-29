from pathlib import Path
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
    """
    It save files under the working directory.
    """

    def upload(self, source_path, destination_path, enable_public=False):

        destination_path = str(destination_path)
        source_path = str(source_path)
        if "." not in destination_path:
            if "." in source_path:
                basename = os.path.basename(source_path)
                destination_path = os.path.join(destination_path, basename)

        if "." in source_path:
            parent_dir = os.path.dirname(destination_path)
        else:
            parent_dir = source_path

        if parent_dir != "":  # check given path directory or not
            Path(parent_dir).mkdir(parents=True, exist_ok=True)

        if os.path.isfile(source_path):
            shutil.copyfile(source_path, destination_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        else:
            raise ValueError(f"{parent_dir} does not exist!")

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

    def upload(self, source_path, destination_path, enable_public=False):
        source_path = str(source_path)
        destination_path = str(destination_path)

        blob = self.bucket.blob(destination_path)
        blob.upload_from_filename(source_path)
        if enable_public:
            blob.make_public()
            return blob.public_url

        return blob.path

    def download(self, source_path, destination_path):

        source_path = str(source_path)
        destination_path = str(destination_path)

        blob = self.bucket.blob(source_path)
        blob.download_to_filename(destination_path)
        return destination_path

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
