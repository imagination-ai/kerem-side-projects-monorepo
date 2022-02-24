from google.cloud import storage
import logging
from common.customized_logging import configure_logging

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

        logger.info(
            f"{source_file_full_path} uploaded to {destination_filename}"
        )

    def download(self, source_filename, destination_filename):

        blob = self.bucket.blob(source_filename)
        blob.download_to_filename(destination_filename)

        logger.info(f"{source_filename} downloaded to {destination_filename}")