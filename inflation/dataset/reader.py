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
    convert_turkish_number_to_us,
)

SAVED_DATASETS_DIR_PATH = (
    Path(__file__).parents[2] / "inflation-resources/data/"
)
NOT_AVAILABLE = "___NA___"

configure_logging()
logger = logging.getLogger(__name__)


class BaseJSONDataReader:
    def read(self, filename, columns=None):
        raise NotImplementedError()


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


class InflationJSONA101DatasetReader(BaseJSONDataReader):
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
        if availability == InflationJSONA101DatasetReader.ITEM_IN_STOCK:
            return True
        elif availability == InflationJSONA101DatasetReader.ITEM_NOT_IN_STOCK:
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

    def read(self, filename, fields=None) -> InflationDataset:
        """It goes through the `filename` and create InflationRecords

        Args:
            filename:
            fields: fields to include. If it is None, include everything.

        Returns:

        """
        records = []
        with open(filename, "rt", encoding="UTF-8") as file:
            total_pages = 0
            item_pages = 0
            for line in file:
                line = json.loads(line)
                total_pages += 1

                item_code, item_name, source = (
                    line["item_code"],
                    line["item_name"],
                    line["source"],
                )

                date = InflationJSONA101DatasetReader.__convert_sample_date(
                    line["timestamp"]
                )
                soup = BeautifulSoup(line["text"], "lxml")
                if InflationJSONA101DatasetReader.__is_product_page(soup):
                    item_pages += 1
                    record = InflationDataRecord(
                        item_code,
                        item_name,
                        source,
                        InflationJSONA101DatasetReader.__get_product_name(soup),
                        InflationJSONA101DatasetReader.__get_product_url(soup),
                        InflationJSONA101DatasetReader.__get_product_code(soup),
                        InflationJSONA101DatasetReader.__get_product_brand(
                            soup
                        ),
                        InflationJSONA101DatasetReader.__get_product_price(
                            soup
                        ),
                        InflationJSONA101DatasetReader.__get_currency(soup),
                        InflationJSONA101DatasetReader.__item_in_stock(soup),
                        date,
                    )
                    records.append(record)
        logger.info(f"total_pages={total_pages}, item_pages={item_pages}")
        return InflationDataset(records)


class InflationJSONMigrosDatasetReader(BaseJSONDataReader):
    ITEM_IN_STOCK = "InStock"
    ITEM_NOT_IN_STOCK = (
        "OutStock"  # TODO: Need to check. It's only a guess right now.
    )

    def read_migros_page(self):  # url, driver_path, driver (quit demek icin)
        driver = webdriver.Chrome(
            executable_path="/Users/kerem/playground/kerem-side-projects-monorepo/common/chromedriver"
        )
        url = "https://www.migros.com.tr/pinar-organik-sut-1-l-p-a822f9"
        driver.get(url)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            soup = BeautifulSoup(driver.page_source, "html.parser")
            soup = soup.find("script", type="application/json+ld")
            page_json = json.loads(
                soup.string
            )  # json contains all related information
            subset_page_json = page_json["mainEntity"]["offers"]["itemOffered"][
                0
            ]

            print(
                InflationJSONMigrosDatasetReader.__get_product_name(
                    subset_page_json
                )
            )
            print(
                InflationJSONMigrosDatasetReader.__get_product_url(
                    subset_page_json
                )
            )
            print(
                InflationJSONMigrosDatasetReader.__get_product_code(
                    subset_page_json
                )
            )
            print(
                InflationJSONMigrosDatasetReader.__get_product_brand(
                    subset_page_json
                )
            )
            print(
                InflationJSONMigrosDatasetReader.__get_product_price(
                    subset_page_json
                )
            )
            print(
                InflationJSONMigrosDatasetReader.__get_currency(
                    subset_page_json
                )
            )
            print(
                InflationJSONMigrosDatasetReader.__item_in_stock(
                    subset_page_json
                )
            )

        finally:
            driver.quit()

        return subset_page_json

    @staticmethod
    def __get_product_name(subset_page_json):
        return subset_page_json["name"]

    @staticmethod
    def __get_product_url(subset_page_json):
        return subset_page_json["url"]

    @staticmethod
    def __get_product_code(subset_page_json):
        return subset_page_json["image"][0]["contentUrl"].split("/")[-2]

    @staticmethod
    def __get_product_brand(subset_page_json):
        return subset_page_json["brand"]["name"]

    @staticmethod
    def __get_product_price(subset_page_json):
        return convert_turkish_number_to_us(subset_page_json["offers"]["price"])

    @staticmethod
    def __get_currency(subset_page_json):
        return subset_page_json["offers"]["priceCurrency"]

    @staticmethod
    def __item_in_stock(subset_page_json):
        availability = subset_page_json["offers"]["availability"].split("/")[-1]
        if availability == InflationJSONMigrosDatasetReader.ITEM_IN_STOCK:
            return True
        elif availability == InflationJSONMigrosDatasetReader.ITEM_NOT_IN_STOCK:
            pass
            return False
        else:
            print(subset_page_json["offers"]["availability"])
            raise TypeError


def run():
    # reader = InflationJSONA101DatasetReader()
    # dataset = reader.read("a101.med.json.gz")
    # print(dataset)
    migros_reader = InflationJSONMigrosDatasetReader()
    migros_reader.read_migros_page()


if __name__ == "__main__":
    run()
