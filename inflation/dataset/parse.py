import json
import datetime
import logging
import _pickle as cPickle
import pandas as pd
import gzip

from dataclasses import dataclass
from pathlib import Path
from bs4 import BeautifulSoup

from common.customized_logging import configure_logging
from common.utils.mathematical_conversation_utils import convert_price_to_us

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

    def save(self, output_file_name):
        """
        It saves dataset records by serializing.
        """

        with open(output_file_name, "wb") as f:
            cPickle.dump(self, f)
        return output_file_name

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
    def __init__(self, parsers: dict):
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
            destination_file_path (str): The destination file path for saving the file
            (gzip
            or json file format).

        Returns:

        """
        google_storage_client.download(data_file_path, destination_file_path)
        return self._start_parsing(destination_file_path)

    def start_parsing_from_drive(self, data_file_path: str):
        return self._start_parsing(data_file_path)

    # TODO consider adding a parameter
    def _start_parsing(self, data_file_path: str):
        records = []

        with ParserManager.open(data_file_path, mode="rt") as file:
            total_pages = 0
            item_pages = 0
            for line in file:
                line = json.loads(line)
                total_pages += 1

                records.append(self.parsers[line["source"].lower()].parse(line))

                item_pages += 1
        logger.info(
            f"Parsing is done: {item_pages}/{total_pages} parsed to {data_file_path}"
        )

        # TODO (kerem) give the filename
        return InflationDataset(records).save()

    @staticmethod
    def open(data_file_path: str, mode: str):
        """
        It takes the data file path (json or gzip) and opens that.
        Args:
            mode:
            data_file_path (str):

        Returns (str):

        """

        func = None
        if data_file_path.endswith(".gz"):
            func = gzip.open
        elif data_file_path.endswith(".json") or data_file_path.endswith(
            ".jsonl"
        ):
            func = open
        else:
            TypeError("You should give json or gzip file format as an input.")

        return func(data_file_path, mode, encoding="UTF-8")


class Parser:
    @staticmethod
    def _convert_sample_date(date: str):
        return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")

    def _get_product_name(self, soup):
        NotImplemented

    def _get_product_url(self, soup):
        NotImplemented

    def _get_product_code(self, soup):
        NotImplemented

    def _get_product_brand(self, soup):
        NotImplemented

    def _get_product_price(self, soup):
        NotImplemented

    def _get_currency(self, soup):
        NotImplemented

    def _item_in_stock(self, soup):
        NotImplemented

    def _is_product_page(self, soup):
        NotImplemented

    def _get_soup(self, soup):
        """This function aids different parses' method (e.g.,
        MigrosParser._get_product_name) as providing
        true soup object."""

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
        date = Parser._convert_sample_date(line["timestamp"])
        soup = self._get_soup(BeautifulSoup(line["text"], "lxml"))

        if self._is_product_page(soup):
            record = InflationDataRecord(
                item_code,
                item_name,
                source,
                self._get_product_name(soup),
                self._get_product_url(soup),
                self._get_product_code(soup),
                self._get_product_brand(soup),
                self._get_product_price(soup),
                self._get_currency(soup),
                self._item_in_stock(soup),
                date,
            )

        return record


class A101Parser(Parser):
    ITEM_IN_STOCK = "in stock"
    ITEM_NOT_IN_STOCK = "out of stock"

    @staticmethod
    def _get_product_name(soup):
        try:
            return soup.find("meta", property="og:title").attrs["content"]
        except AttributeError:
            return NOT_AVAILABLE

    @staticmethod
    def _get_product_url(soup):
        try:
            return soup.find("meta", property="og:url")["content"]
        except AttributeError as e:
            with open("/tmp/error.html", "wt") as f:
                f.write(soup.text)
            raise e
            # return NOT_AVAILABLE

    @staticmethod
    def _get_product_code(soup):
        try:
            return (
                soup.find("div", {"class": "product-code"})
                .get_text()
                .split(": ")[1]
            )
        except AttributeError:
            return NOT_AVAILABLE

    @staticmethod
    def _get_product_brand(soup):
        try:
            return soup.find("meta", property="og:brand").attrs["content"]
        except AttributeError:
            return NOT_AVAILABLE

    @staticmethod
    def _get_product_price(soup):
        return float(
            soup.find("meta", property="product:price:amount").attrs["content"]
        )

    @staticmethod
    def _get_currency(soup):
        return soup.find("meta", property="product:price:currency").attrs[
            "content"
        ]

    @staticmethod
    def _item_in_stock(soup):
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
    def _convert_sample_date(date: str):
        return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")

    @staticmethod
    def _is_product_page(soup):
        return all(
            [
                soup.find("meta", property="og:url"),
                soup.find("meta", property="product:price:amount"),
            ]
        )

    @staticmethod
    def _get_soup(soup):
        return soup


class MigrosParser(Parser):
    @staticmethod
    def _get_product_name(soup):
        return soup["name"]

    @staticmethod
    def _get_product_url(soup):
        return soup["url"]

    @staticmethod
    def _get_product_code(soup):
        return soup["image"][0]["contentUrl"].split("/")[-2]

    @staticmethod
    def _get_product_brand(soup):
        return soup["brand"]["name"]

    @staticmethod
    def _get_currency(soup):
        return soup["offers"]["priceCurrency"]

    @staticmethod
    def _get_product_price(soup):
        return convert_price_to_us(soup["offers"]["price"])

    @staticmethod
    def _item_in_stock(soup):
        if convert_price_to_us(soup["offers"]["price"]) == 0:
            return False
        else:
            return True

    @staticmethod
    def _get_soup(soup):
        soup = soup.find("script", type="application/json+ld")
        page_json = json.loads(
            soup.string
        )  # json contains all related information
        subset_page_json = page_json["mainEntity"]["offers"]["itemOffered"][0]
        return subset_page_json

    @staticmethod
    def _is_product_page(soup):  # TODO: Implement this
        return True


def run():
    # TODO (kerem) add argparse.
    parsers = {"a101": A101Parser(), "migros": MigrosParser()}
    pm = ParserManager(parsers)
    dataset = pm.start_parsing_from_drive(
        "inflation/dataset/inflation-crawl.jsonl-20220305103250.jsonl.gz"
    )
    print(f"{dataset.dataset}")


if __name__ == "__main__":
    run()
