import datetime
import logging
import os.path
import tempfile

import pandas as pd

from common.clients.google_storage_client import GoogleStorageClient
from common.customized_logging import configure_logging
from inflation.config import settings

configure_logging()
logger = logging.getLogger(__name__)


parser_client = GoogleStorageClient(bucket_name=settings.PARSER_BUCKET)

with tempfile.TemporaryDirectory() as tmp_dir:
    blobs = parser_client.list_objects()

    for blob in blobs:
        input_fn = parser_client.download(blob.name, tmp_dir)
        # 2022-03-27.parse.jsonl

        converters = {
            "item_code": lambda x: str(x),
            "product_code": lambda x: str(x),
            "sample_date": lambda x: datetime.datetime.strptime(
                x, "%Y-%m-%d %H:%M:%S"
            ),
        }
        df = pd.read_csv(
            input_fn, sep="\t", parse_dates=True, converters=converters
        )
        df.drop("Unnamed: 0", axis=1, inplace=True)
        fp = os.path.join(tmp_dir, blob.name)
        df.to_csv(fp, sep="\t", index=False)

        logger.info(f"{blob.name} is replaced.")
        parser_client.upload(fp, blob.name)
        logger.info(f"{fp} is uploaded to {settings.PARSER_BUCKET} bucket.")
