from google.cloud import storage
import logging
from common.customized_logging import configure_logging
from pathlib import Path

INFLATION_DATASETS_DIR = (
    Path(__file__).parents[2] / "inflation-resources/data/inflation/"
)

configure_logging()
logger = logging.getLogger(__name__)


# Q: Acaba boyle bir genel class mi yazsam? Alttaki bunun altina falan?
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def upload_inflation_data_file(
    bucket_name, source_file_name, destination_blob_name
):

    source_file_full_path = Path(INFLATION_DATASETS_DIR / source_file_name)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_full_path)

    logger.info(
        f"{source_file_name} inflation data file uploaded to {source_file_name}, "
        f"{destination_blob_name}"
    )


# TODO: argparse
