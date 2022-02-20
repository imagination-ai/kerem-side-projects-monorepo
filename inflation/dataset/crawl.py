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
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Q: bu alttakilere gerek var mi?
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-data-dir=chrome-data")

    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.driver = webdriver.Chrome(
            executable_path=self.executable_path, options=self.options
        )
        self.wait = WebDriverWait(self.driver, 5)


class NewCrawler:
    def __init__(
        self,
        chrome_driver_path="/Users/kerem/playground/kerem-side-projects-monorepo/common/chromedriver",
    ):
        self.page_crawler_robot = PageCrawlerRobot(chrome_driver_path)

    """
Crawler --> spreadsheet'i okuyacak --> urunleri gezecek -->  urunun sayfasini acacak, hicbir sey filtrelemecek ve bir
dosyaya o gunu kaydedecek. Sayfa formati soyle olacak: her satir json.   Satir1: {"html": sayfanin content'i-ne-varsa,
"website": "migros", "url": urunun-cekildigi-url, "spreadsheet'ten gelen diger onemli bilgiler"} Satir2:
{"html": sayfanin content'i-ne-varsa, "website": "a101", "url": urunun-cekildigi-url,
"spreadsheet'ten gelen diger onemli bilgiler"}
Bu dosya sonra gcloud.storage'a ziplenerek upload edilecek. Bu   Crawl   endpoint'imiz.
    Returns:

    """

    @staticmethod
    def parse_excel_to_link_dataset(file_path) -> List[ItemRecord]:
        """
        The function first reads the spreadsheet file containing item codes, names (COICOP),
        and related products with their links, then parse the source information (e.g., Migros, A101, etc.)
        and save the product's information as ItemRecord. It returns a list of ItemRecords.


        Args:
            file_path (str): An Excel file path or  a Google SpreadSheet URL.

        Returns (list): List of ItemRecords.

        Note: Only works with the first sheet of a spreadsheet file.
        """
        file_path = NewCrawler.format_spreadsheet_path(file_path)
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

    @staticmethod
    def select_right_crawler(source: str):
        crawl_functions = {
            "A101": NewCrawler.crawl_A101,
            "Migros": NewCrawler.crawl_Migros,
        }

        return crawl_functions[source]

    @staticmethod
    def crawl(records: List[ItemRecord], path="/", output_fn="python-crawl"):
        # why did we need need this path, parameters? and why did we give "python-crawl" default input?
        """

        Args:
            records:
            path:
            output_fn:

        Returns:

        """
        date_stamp_output_file = datetime.now().strftime("%Y%m%d%H%M%S")
        output_fn_full_path = os.path.join(
            path, f"{output_fn}-{date_stamp_output_file}.jsonl"
        )
        total_saved = 0

        with open(output_fn_full_path, "w") as file:
            logger.info(f"Total of {len(records)} records will be processed.")
            for record in records:
                date_stamp_record_file = datetime.now().strftime("%Y%m%d%H%M%S")
                crawler_func = NewCrawler.select_right_crawler(record.source)
                d = {
                    "text": crawler_func(
                        record.product_url, record.product_name
                    ),
                    "timestamp": date_stamp_record_file,
                    "item_name": record.item_name,
                    "item_code": record.item_code,
                    "product_name": record.product_name,
                    "source": record.source,
                }
                data = json.dumps(d)
                file.write(f"{data}\n")
                total_saved += 1

            logger.info(
                f"Total of {total_saved}/{len(records)} records are saved to "
                f"{output_fn_full_path}"
            )

        return output_fn_full_path

    @staticmethod
    def crawl_A101(product_url, product_name):
        r = requests.get(product_url)

        if r.status_code == 200:
            return BeautifulSoup(r.text, "html.parser")
        else:
            logger.info(  # Q: Should we change logging type? (Warning or else?)
                f"{product_name}'s page ({product_url}) hasn't "
                f"been crawled (Status Code: {r.status_code}"
            )

    def crawl_Migros(
        self, product_url, product_name
    ):  # bu robotu class variable olarak mi alsak?
        self.page_crawler_robot.get(product_url)

        try:
            self.page_crawler_robot.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            return BeautifulSoup(
                self.page_crawler_robot.page_source, "html.parser"
            )
        except (
            RuntimeError,
            TypeError,
        ):  # Q: bos verince olmuyordu bu kismi nasil yapmak lazim acaba?
            logger.info(  # Q: Should we change logging type? (Warning or else?)
                f"{product_name}'s page ({product_url}) hasn't been crawled."
            )


##### Eski dosyalar


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
        file_path = NewCrawler.format_spreadsheet_path(file_path)
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
