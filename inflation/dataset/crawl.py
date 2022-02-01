from typing import List
import logging
import requests
import json
import pandas as pd
from dataclasses import dataclass
from datetime import datetime

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


class Crawler:
    def parse_excel_to_link_dataset(self, file_path):
        """It takes excel file path convert them into list of TurkstatItemRecord class and save it into a list.

        Note: Only works with the first sheet of an Excel file.

        Args:
            file_path: File path of the Excel file that includes the products information and their links/

        Returns: List of TurkstatItemRecord

        """

        records = []

        excel_file = pd.ExcelFile(file_path)
        sheet_name = excel_file.sheet_names[0]

        print(f"Using {sheet_name} for parsing the links.")
        df = excel_file.parse(sheet_name)

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

    def crawl(self, records: List[ItemRecord], full_name_record_file):
        """

        Args:
            records:
            full_name_record_file:

        Returns:
            Note: Logging file of this script is extremely important since the catches "un-crawled" pages.

        """
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        with open(f"{full_name_record_file}-{date}.json", "w") as file:
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
                else:
                    logger.info(
                        f"{record.product_name}'s page ({record.product_url}) hasn't been crawled (Status Code: {r.status_code}"
                    )


def run():
    import argparse

    parser = argparse.ArgumentParser(description="crawl items from website")
    parser.add_argument(
        "--excel-path", type=str, help="The file path excel database file"
    )
    parser.add_argument(
        "--record-full-name", type=str, help="The name of the json record file"
    )

    args = parser.parse_args()
    logger.info(f"{args}")

    crawler = Crawler()
    records = crawler.parse_excel_to_link_dataset(file_path=args.excel_path)
    crawler.crawl(records, full_name_record_file=args.record_full_name)


if __name__ == "__main__":
    run()
