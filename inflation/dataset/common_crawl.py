from copy import deepcopy
import gzip
import json
import logging

import cdx_toolkit
from common.customized_logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


# curl https://index.commoncrawl.org/CC-MAIN-2021-49-index\?url\=www.migros.com.tr%2F
# \*\&output\=json | jq .url > migros.txt


class CommonCrawlerDownloader:
    def __init__(self):
        self.cdx = cdx_toolkit.CDXFetcher(source="cc")  # cc means common crawl

    def download_as_warc(
        self,
        *,
        url,
        warc_description,
        writer_prefix,
        writer_subprefix,
        exclude_status_codes=None,
        limit: int = None,
    ):

        exclude_status_codes = exclude_status_codes or {}

        params = {"url": url}

        if limit is not None:
            params["limit"] = limit

        warcinfo = {
            "software": "imagination-ai",
            "isPartOf": "imagination-ai/kerem-monorepo",
            "description": warc_description,
            "format": "WARC file version 1.0",
        }
        writer = cdx_toolkit.warc.get_writer(
            writer_prefix, writer_subprefix, warcinfo, warc_version="1.0"
        )

        num_written_record = 0
        num_fetched_record = 0
        for record in self.cdx.iter(**params):
            url = record["url"]
            status = record["status"]

            if num_fetched_record % 5000 == 0:
                logger.info(
                    f"{num_fetched_record} record is fetched. Total "
                    f"{num_written_record} record is "
                    f"written."
                )

            if status not in exclude_status_codes:
                try:
                    record = record.fetch_warc_record()
                except RuntimeError as e:
                    logger.warning(f"Skipping a record at {url}. {e}")
                    continue
                writer.write_record(record)
                num_written_record += 1
            num_fetched_record += 1

        logger.info(
            f"Completed with total of {num_fetched_record} record is fetched. Total "
            f"{num_written_record} record is written."
        )

    def download_partially_as_json(
        self,
        *,
        url,
        output_fn,
        exclude_status_codes=None,
        limit: int = None,
    ):

        exclude_status_codes = exclude_status_codes or {}

        params = {"url": url}

        if limit is not None:
            params["limit"] = limit

        with gzip.open(output_fn, "wt") as f:
            num_written_record = 0
            num_fetched_record = 0
            for record in self.cdx.iter(**params):
                status = record["status"]

                record_to_save = deepcopy(record.data)
                record_to_save["text"] = record.text

                if num_fetched_record % 5000 == 0:
                    logger.info(
                        f"{num_fetched_record} record is fetched. Total "
                        f"{num_written_record} record is "
                        f"written."
                    )

                if status not in exclude_status_codes:
                    f.write(f"{json.dumps(record_to_save)}\n")
                    num_written_record += 1
                num_fetched_record += 1

        logger.info(
            f"Completed with total of {num_fetched_record} record is fetched. Total "
            f"{num_written_record} record is written."
        )
