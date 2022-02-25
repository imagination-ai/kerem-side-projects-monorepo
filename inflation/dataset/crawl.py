from dataclasses import dataclass
from datetime import datetime
import json
import logging
import os
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
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


class PageCrawlerRobot:
    def __init__(self, executable_path="chromedriver", headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        options.add_argument("--no-sandbox")  # Q: bu alttakilere gerek var mi?
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-data-dir=chrome-data")
        self.driver = webdriver.Chrome(
            executable_path=executable_path, options=options
        )
        self.wait = WebDriverWait(self.driver, 5)

    def get_page(self, url, by=By.CLASS_NAME, field="price"):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((by, field))
            )
            return BeautifulSoup(self.driver.page_source, "lxml").text
        except NoSuchElementException:
            # TODO (kerem): exception handling? think about it
            pass


class Crawler:
    """

    Returns:

    """

    def get_page(self, url):
        r = requests.get(url)

        if r.status_code == 200:
            return BeautifulSoup(r.text, "lxml").text

    def crawl(self, record: ItemRecord):
        """
        Args:
            record (ItemRecord):
        Returns (dict):

        """

        page = self.get_page(record.product_url)
        if page is not None:
            return {
                "text": page,
                "timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
                "item_name": record.item_name,
                "item_code": record.item_code,
                "product_name": record.product_name,
                "source": record.source,
            }


class MigrosCrawler(Crawler):
    def __init__(self):
        self.robot = PageCrawlerRobot()

    def get_page(self, url):
        return self.robot.get_page(url)


class A101Crawler(Crawler):
    pass


class CrawlerManager:
    def __init__(self, crawlers: dict):
        self.crawlers = crawlers

    @staticmethod
    def parse_excel_to_link_dataset(file_path):
        """
        The function first reads the spreadsheet file containing item codes, names (COICOP),
        and related products with their links, then parse the source information (e.g., Migros, A101, etc.)
        and save the product's information as ItemRecord. It returns a list of ItemRecords.


        Args:
            file_path (str): An Excel file path or  a Google SpreadSheet URL.

        Returns (list): List of ItemRecords.

        Note: Only works with the first sheet of a spreadsheet file.

        """
        file_path = CrawlerManager.format_spreadsheet_path(file_path)
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
            source = link.split(".")[1].lower()

            record = ItemRecord(
                item_code, item_name, product_name, link, source
            )
            records.append(record)

        return records

    @staticmethod
    def format_spreadsheet_path(path: str):
        """
        It checks the string is url or file path then convert to legitimate form.
        Args:
            path (str): url of a Google spreadsheet or file path.

        Returns:

        Note: The Google spreadsheet file must be shared publicly first before copy the
        full url.
        Private files raise authentication errors.
        """

        path = str(path)
        if path.startswith("http"):
            path = path.replace("/edit#gid=0", "/export?format=xlsx&gid=0")

        return path

    def start_crawling(
        self, records: List[ItemRecord], path="/", output_fn="inflation-crawl"
    ):
        date_stamp_output_file = datetime.now().strftime("%Y%m%d%H%M%S")
        output_fn_full_path = os.path.join(
            path, f"{output_fn}-{date_stamp_output_file}.jsonl"
        )
        total_saved = 0

        with open(output_fn_full_path, "w") as file:
            logger.info(f"Total of {len(records)} records will be processed.")
            for record in records:
                d = self.crawlers[record.source.lower()].crawl(record)

                data = json.dumps(d)
                file.write(f"{data}\n")
                total_saved += 1

            logger.info(
                f"Total of {total_saved}/{len(records)} records are saved to {output_fn_full_path}"
            )

        return output_fn_full_path


def run():
    import argparse

    parser = argparse.ArgumentParser(description="crawl items from website")
    parser.add_argument(
        "--excel-path",
        type=str,
        help="The file path or url of spreadsheet database file",
    )
    parser.add_argument(
        "--path", type=str, help="The name of the json record file"
    )

    args = parser.parse_args()
    logger.info(f"{args}")

    crawlers = {"a101": A101Crawler(), "migros": MigrosCrawler()}
    cm = CrawlerManager(crawlers)
    records = cm.parse_excel_to_link_dataset(file_path=args.excel_path)
    cm.start_crawling(records, path=args.path)


if __name__ == "__main__":
    run()
