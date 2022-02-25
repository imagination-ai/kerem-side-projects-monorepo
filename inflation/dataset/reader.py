import gzip
import json
import datetime
import logging
import _pickle as cPickle
import pandas as pd

from dataclasses import dataclass
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.customized_logging import configure_logging
from common.utils.mathematical_conversation_utils import (
    convert_price_to_us,
)

SAVED_DATASETS_DIR_PATH = (
    Path(__file__).parents[2] / "inflation-resources/data/"
)
NOT_AVAILABLE = "___NA___"

configure_logging()
logger = logging.getLogger(__name__)


@dataclass
class InflationDataRecord:
    item_code: str
    item_name: str
    source: str
    product_name: str
    product_url: str
    product_code: str  # item identifier for this data.
    product_brand: str
    price: float
    currency: str
    in_stock: bool
    sample_date: datetime.datetime


class InflationDataset:
    def __init__(self, data: list):
        self.dataset = data

    def __len__(self):
        return len(self.dataset)

    def __iter__(self):
        return InflationDatasetIterator(self.dataset)

    def __getitem__(self, s):
        if s < 0:
            s = self.__len__() - s
            if s < 0 or s >= self.__len__():
                raise IndexError
            else:
                return self.dataset[s]
        else:
            start, stop, step = s.indices(self.__len__())
            indxs = list(range(start, stop, step))
            return [self.dataset[i] for i in indxs]

    def save_dataset(self, output_file_name):
        """
        It saves dataset records by serializing.
        """
        full_path = SAVED_DATASETS_DIR_PATH / output_file_name

        with open(full_path, "wb") as f:
            cPickle.dump(self, f)

    @classmethod
    def read_dataset(cls, file_path):
        with open(file_path, "rb") as input_file:
            return cPickle.load(input_file)

    def to_df(self):
        return pd.DataFrame([record.__dict__ for record in self.dataset])


class InflationDatasetIterator:
    def __init__(self, inflation_dataset):
        self.dataset = inflation_dataset
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= len(self.dataset):
            raise StopIteration
        else:
            result = self.dataset[self._i]
            self._i += 1
            return result


class ParserManager:
    def __init__self(self, parsers: dict):
        self.parsers = parsers

    def start_parsing_from_google_storage(
        self,
        google_storage_client,
        data_file_path: str,
        destination_file_path: str,
    ):
        """

        Args:
            data_file_path (str): The data file path in the Google Storage.
            destination_file_path (str): The destination file path for saving the file.

        Returns:

        """
        google_storage_client.download(data_file_path, destination_file_path)
        return self._start_parsing(destination_file_path)

    def start_parsing_from_drive(self, data_file_path: str):
        return self._start_parsing(data_file_path)

    def _start_parsing(self, data_file_path: str):
        records = []

        with open(data_file_path, "rt", encoding="UTF-8") as file:
            total_pages = 0
            item_pages = 0
            for line in file:
                line = json.loads(line)
                total_pages += 1
                records.append(self.parsers[line["source"].lower()])
                item_pages += 1
        logger.info(f"total_pages={total_pages}, item_pages={item_pages}")

        return InflationDataset(records)


class Parser:
    @staticmethod
    def __convert_sample_date(date: str):
        return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")

    def __get_product_name(self, soup):
        NotImplemented

    def __get_product_url(self, soup):
        NotImplemented

    def __get_product_code(self, soup):
        NotImplemented

    def __get_product_brand(self, soup):
        NotImplemented

    def __get_product_price(self, soup):
        NotImplemented

    def __get_currency(self, soup):
        NotImplemented

    def __item_in_stock(self, soup):
        NotImplemented

    def __is_product_page(self, soup):
        NotImplemented

    def parse(self, line) -> InflationDataRecord:

        """It goes through the `filename` and create InflationRecords

        Args:
            line:


        Returns: record

        """
        item_code, item_name, source = (
            line["item_code"],
            line["item_name"],
            line["source"],
        )
        date = Parser.__convert_sample_date(line["timestamp"])
        soup = BeautifulSoup(line["text"], "lxml")
        if self.__is_product_page(soup):

            record = InflationDataRecord(
                item_code,
                item_name,
                source,
                self.__get_product_name(soup),
                self.__get_product_url(soup),
                self.__get_product_code(soup),
                self.__get_product_brand(soup),
                self.__get_product_price(soup),
                self.__get_currency(soup),
                self.__item_in_stock(soup),
                date,
            )

        return record


class A101Parser(Parser):
    ITEM_IN_STOCK = "in stock"
    ITEM_NOT_IN_STOCK = "out of stock"

    @staticmethod
    def __get_product_name(soup):
        try:
            return soup.find("meta", property="og:title").attrs["content"]
        except AttributeError:
            return NOT_AVAILABLE

    @staticmethod
    def __get_product_url(soup):
        try:
            return soup.find("meta", property="og:url")["content"]
        except AttributeError as e:
            with open("/tmp/error.html", "wt") as f:
                f.write(soup.text)
            raise e
            # return NOT_AVAILABLE

    @staticmethod
    def __get_product_code(soup):
        try:
            return (
                soup.find("div", {"class": "product-code"})
                .get_text()
                .split(": ")[1]
            )
        except AttributeError:
            return NOT_AVAILABLE

    @staticmethod
    def __get_product_brand(soup):
        try:
            return soup.find("meta", property="og:brand").attrs["content"]
        except AttributeError:
            return NOT_AVAILABLE

    @staticmethod
    def __get_product_price(soup):
        return float(
            soup.find("meta", property="product:price:amount").attrs["content"]
        )

    @staticmethod
    def __get_currency(soup):
        return soup.find("meta", property="product:price:currency").attrs[
            "content"
        ]

    @staticmethod
    def __item_in_stock(soup):
        availability = (
            soup.find("meta", property="product:availability")
            .attrs["content"]
            .strip()
        )
        if availability == A101Parser.ITEM_IN_STOCK:
            return True
        elif availability == A101Parser.ITEM_NOT_IN_STOCK:
            return False
        else:
            print(availability)
            raise TypeError

    @staticmethod
    def __convert_sample_date(date: str):
        return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")

    @staticmethod
    def __is_product_page(soup):
        return all(
            [
                soup.find("meta", property="og:url"),
                soup.find("meta", property="product:price:amount"),
            ]
        )


def run():
    reader = A101Parser()
    dataset = reader.parse("a101.med.json.gz")
    # parsers = {"a101": A101Parser(), "migros": NotImplementedError}
    print(dataset)


if __name__ == "__main__":
    run()
