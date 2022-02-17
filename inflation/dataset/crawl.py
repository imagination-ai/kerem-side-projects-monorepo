from dataclasses import dataclass
from datetime import datetime
import json
import logging
import os
from typing import List

import pandas as pd
import requests

from common.customized_logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@dataclass
class ItemRecord:
    item_code: str
    item_name: str
    product_name: str
    product_url: str
    source: str


def format_spreadsheet_path(path: str):
    """
    It checks the string is url or file path then convert to legitimate form.
    Args:
        path (str): url of a google spreadsheet  or file path

    Returns:

    Note: The Google spreadsheet file must be shared publicly first before copy the
    full url.
    Private files raise authentication errors.
    """

    path = str(path)
    if path.startswith("http"):
        path = path.replace("/edit#gid=0", "/export?format=xlsx&gid=0")

    return path


class Crawler:
    def parse_excel_to_link_dataset(self, file_path):
        """It takes excel file path convert them into list of TurkstatItemRecord class
        and save it into a list.

        Note: Only works with the first sheet of an Excel file.

        Args:
            file_path: File path of the Excel file that includes the products
            information and their links/

        Returns: List of TurkstatItemRecord

        """
        file_path = format_spreadsheet_path(file_path)
        logger.info(
            f"File path to fetch and read the spreadsheet is {file_path}"
        )

        df = pd.read_excel(file_path, dtype="object")
        df = df[df["product_links"].notnull()]

        records = []

        for row in df.iterrows():
            item_code = row[1][0]
            item_name = row[1][1]
            product_name = row[1][2]
            link = row[1][3]
            source = link.split(".")[1].capitalize()

            record = ItemRecord(
                item_code, item_name, product_name, link, source
            )
            records.append(record)

        return records

    def crawl(
        self, records: List[ItemRecord], path="/", output_fn="python-crawl"
    ):
        """

        Args:
            output_fn:
            path:
            records:

        Returns:
            Note: Logging file of this script is extremely important since the catches
            "un-crawled" pages.

        """
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        output_fn_full_path = os.path.join(path, f"{output_fn}-{date}.jsonl")
        total_saved = 0

        with open(output_fn_full_path, "w") as file:
            logger.info(f"Total of {len(records)} records will be processed.")
            for record in records:
                date = datetime.now().strftime("%Y%m%d%H%M%S")
                r = requests.get(record.product_url)

                if r.status_code == 200:

                    d = {
                        "text": r.text,
                        "timestamp": date,
                        "item_name": record.item_name,
                        "item_code": record.item_code,
                        "product_name": record.product_name,
                        "source": record.source,
                    }
                    data = json.dumps(d)
                    file.write(f"{data}\n")
                    total_saved += 1
                else:
                    logger.info(
                        f"{record.product_name}'s page ({record.product_url}) hasn't "
                        f"been crawled (Status Code: {r.status_code}"
                    )
            logger.info(
                f"Total of {total_saved}/{len(records)} records are saved to "
                f"{output_fn_full_path}"
            )
        return output_fn_full_path


def run():
    import argparse

    parser = argparse.ArgumentParser(description="crawl items from website")
    parser.add_argument(
        "--excel-path", type=str, help="The file path excel database file"
    )
    parser.add_argument(
        "--path", type=str, help="The name of the json record file"
    )

    args = parser.parse_args()
    logger.info(f"{args}")

    crawler = Crawler()
    records = crawler.parse_excel_to_link_dataset(file_path=args.excel_path)
    crawler.crawl(records, path=args.path)


if __name__ == "__main__":
    run()
