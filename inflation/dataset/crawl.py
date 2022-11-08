import gzip
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-data-dir=chrome-data")
        self.driver = webdriver.Chrome(
            service=Service(executable_path), options=options
        )
        self.wait = WebDriverWait(self.driver, 10)

    def is_page_ready(self):
        raise NotImplementedError()

    def get_page(self, url):
        self.driver.get(url)

        try:
            if self.is_page_ready():
                return self.driver.page_source
        except TimeoutException:
            logger.warning(f"Timeout for {url}. Check your predicate.")


class MigrosCrawlerRobot(PageCrawlerRobot):
    def is_page_ready(self):
        def _predicate(driver):
            amount = driver.find_element(By.CLASS_NAME, "amount")
            if len(amount.text) > 0 and amount.text.endswith("TL"):
                return True
            return False

        self.wait.until(_predicate)
        return True


class MacroCenterCrawlerRobot(PageCrawlerRobot):
    def is_page_ready(self):
        def _predicate(driver):
            amount = driver.find_element(By.CLASS_NAME, "amount")
            if len(amount.text) > 0 and amount.text.endswith("TL"):
                return True
            return False

        self.wait.until(_predicate)
        return True


# TODO: add timeouterror


class Crawler:
    """

    Returns:

    """

    @staticmethod
    def parse_excel_to_link_dataset(file_path) -> List[ItemRecord]:
        """
        The function first reads the spreadsheet file containing item codes,
        names (COICOP),
        and related products with their links, then parse the source information (
        e.g., Migros, A101, etc.)
        and save the product's information as ItemRecord. It returns a list of
        ItemRecords.


        Args:
            file_path (str): An Excel file path or  a Google SpreadSheet URL.

        Returns (list): List of ItemRecords.

        Note: Only works with the first sheet of a spreadsheet file.
        """
        file_path = CrawlerManager.format_spreadsheet_path(file_path)
        logger.info(
            f"File path to fetch and read the spreadsheet is {file_path}"
        )

        df = pd.read_excel(file_path, dtype="obj")
        df = df[df["product_links"].notnull()]

        records = []

        for row in df.iterrows():
            item_code = row[1][0]
            item_name = row[1][1]
            product_name = row[1][2]
            link = row[1][3]
            source = link.split(".")[1]

            record = ItemRecord(
                item_code, item_name, product_name, link, source
            )
            records.append(record)

        return records

    def get_page(self, url):
        r = requests.get(url)

        if r.status_code == 200:
            return r.text

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
        self.robot = MigrosCrawlerRobot()

    def get_page(self, url):
        return self.robot.get_page(url)


class MacroCenterCrawler(Crawler):
    def __init__(self):
        self.robot = MacroCenterCrawlerRobot()

    def get_page(self, url):
        return self.robot.get_page(url)


class A101Crawler(Crawler):
    pass


class CarrefourCrawler(Crawler):
    pass


class CrawlerManager:
    def __init__(self, crawlers: dict):
        self.crawlers = crawlers

    @staticmethod
    def parse_excel_to_link_dataset(file_path):
        """
        The function first reads the spreadsheet file containing item codes,
        names (COICOP),
        and related products with their links, then parse the source information (
        e.g., Migros, A101, etc.)
        and save the product's information as ItemRecord. It returns a list of
        ItemRecords.


        Args:
            file_path (str): An Excel file path or  a Google SpreadSheet URL.

        Returns (list): List of ItemRecords.

        Note: Only works with the first sheet of a spreadsheet file.

        """
        file_path = CrawlerManager.format_spreadsheet_path(file_path)
        logger.info(
            f"File path to fetch and read the spreadsheet is {file_path}"
        )

        df = pd.read_excel(file_path, dtype="str")
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
        self,
        records: List[ItemRecord],
        path="./",
        output_fn="inflation-crawl.jsonl.gz",
    ):

        output_fn_full_path = os.path.join(path, output_fn)
        total_saved = 0
        total = len(records)

        with gzip.open(output_fn_full_path, "wt") as file:
            logger.info(f"Total of {total} records will be processed.")
            for record in records:
                d = None
                crawler = self.crawlers.get(record.source.lower())
                if crawler is not None:
                    d = crawler.crawl(record)
                if d is not None:
                    data = json.dumps(d)
                    file.write(f"{data}\n")
                    total_saved += 1
                else:
                    logger.warning(f"Skipping {record}...")

            logger.info(
                f"Total of {total_saved}/{total} records are saved to "
                f"{output_fn_full_path}"
            )
            if total_saved != total:
                logger.warning(f"{total - total_saved} records skipped.")

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

    crawlers = {
        "a101": A101Crawler(),
        "migros": MigrosCrawler(),
        "carrefoursa": CarrefourCrawler(),
        "macrocenter": MacroCenterCrawler(),
    }
    cm = CrawlerManager(crawlers)
    records = cm.parse_excel_to_link_dataset(file_path=args.excel_path)
    cm.start_crawling(records, path=args.path)


if __name__ == "__main__":
    run()
