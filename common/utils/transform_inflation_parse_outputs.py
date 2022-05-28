import logging
import os
import tempfile
from common.clients.google_storage_client import GoogleStorageClient
from inflation.config import settings
from common.customized_logging import configure_logging
from inflation.dataset.parse import InflationDataset

configure_logging()
logger = logging.getLogger(__name__)


parser_client = GoogleStorageClient(bucket_name=settings.PARSER_BUCKET)

with tempfile.TemporaryDirectory() as tmp_dir:
    blobs = parser_client.list_objects()

    for blob in blobs:
        if not blob.name.endswith("tsv"):
            input_fn = parser_client.download(blob.name, tmp_dir)
            # 2022-03-27.parse.jsonl
            new_fn = input_fn.rsplit(".", maxsplit=1)[0] + ".tsv"
            output_fn = InflationDataset.read(input_fn).save(new_fn)
            logger.info(f"{blob.name} is changed with {new_fn}.")
            parser_client.upload(output_fn, os.path.basename(output_fn))
            logger.info(
                f"{output_fn} is uploaded to {settings.PARSER_BUCKET} bucket."
            )
