import os.path

from google.cloud import storage
import logging
from common.customized_logging import configure_logging
from google.auth.credentials import AnonymousCredentials


configure_logging()
logger = logging.getLogger(__name__)


class GoogleStorageClient:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def upload(self, source_file_full_path, destination_filename):
        blob = self.bucket.blob(destination_filename)
        blob.upload_from_filename(source_file_full_path)

    def download(self, source_filename, destination):
        blob = self.bucket.blob(source_filename)
        if isinstance(destination, str):
            full_path = os.path.join(destination, source_filename)
            blob.download_to_filename(full_path)
            return full_path
        else:
            blob.download_to_file(destination)
            return destination.name
