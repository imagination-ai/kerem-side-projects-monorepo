from common.clients.google_storage_client import (
    get_storage_client,
    GoogleStorageClient,
    MockStorageClient,
)
from common.config import settings


class FileWriter:
    def __init__(self, storage_client):
        self.storage_client = get_storage_client(storage_client)

    def read(self):
        pass

    def write(self, source_file_full_path, destination_filename):
        if isinstance(self.storage_client, GoogleStorageClient):
            self.storage_client.upload(
                source_file_full_path, destination_filename
            )
