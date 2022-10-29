import json
import datetime
import logging
import _pickle as cPickle
import os

import pandas as pd
import gzip

from dataclasses import dataclass
from pathlib import Path
from bs4 import BeautifulSoup

from common.customized_logging import configure_logging
from common.utils.mathematical_conversation_utils import convert_price_to_us

OUTPUT_PATH_DIR = Path(__file__).parents[2] / "inflation-resources/data/"
PARSER_OUTPUT_DIR = f"{OUTPUT_PATH_DIR}/parser"

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

    def save_as_pickle(self, output_file_name):
        """
        It saves dataset records by serializing.
        """

        with open(output_file_name, "wb") as f:
            cPickle.dump(self, f)
        return output_file_name

    @classmethod
    def _read_from_pickle(cls, filepath):
        with open(filepath, "rb") as input_file:
            return cPickle.load(input_file)

    @classmethod
    def _read_from_tsv(cls, filepath):
        converters = {
            "item_code": lambda x: str(x),
            "product_code": lambda x: str(x),
            "sample_date": lambda x: datetime.datetime.strptime(
                x, "%Y-%m-%d %H:%M:%S"
            ),
        }
        df = pd.read_csv(
            filepath, sep="\t", parse_dates=True, converters=converters
        )
        num_rows, _ = df.shape
        records = []
        for i in range(num_rows):
            record = InflationDataRecord(*df.loc[i].to_list())
            records.append(record)

        return cls(records)

    @classmethod
    def read(cls, filepath, input_format="tsv"):
        if input_format == "tsv":
            return cls._read_from_tsv(filepath)
        elif input_format == "pickle":
            return cls._read_from_pickle(filepath)

    def to_df(self):
        return pd.DataFrame([record.__dict__ for record in self.dataset])

    def save(self, output_file_name):
        self.to_df().to_csv(output_file_name, sep="\t", index=False)
        return output_file_name


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

    def start_parsing(
        self,
        data_filepath: str,
        output_filepath: str,
        filename: str,
        output_format="tsv",
    ):
        records = []
        with ParserManager.open(data_filepath, mode="rt") as file:
            total_pages = 0
            item_pages = 0
            for line in file:
                line = json.loads(line)
                total_pages += 1
                records.append(self.parsers[line["source"].lower()].parse(line))
                item_pages += 1

        output_fn_full_path = os.path.join(output_filepath, filename)
        logger.info(
            f"Parsing is done: {item_pages}/{total_pages} parsed to {output_fn_full_path}"
        )
        if output_format == "tsv":
            return InflationDataset(records).save(output_fn_full_path)
        else:
            return InflationDataset(records).save_as_pickle(output_fn_full_path)

    @staticmethod
    def open(data_filepath: str, mode: str):
        """
        It takes the data file path (json or gzip) and opens that.
        Args:
            mode:
            data_filepath (str):

        Returns (str):

        """

        func = None
        if data_filepath.endswith(".gz"):
            func = gzip.open
        elif data_filepath.endswith(".json") or data_filepath.endswith(
            ".jsonl"
        ):
            func = open
        else:
            TypeError("You should give json or gzip file format as an input.")

        return func(data_filepath, mode, encoding="UTF-8")


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
        true soup obj."""

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
        soup = soup.find("script", type="application/ld+json")
        page_json = json.loads(
            soup.string
        )  # json contains all related information
        subset_page_json = page_json["mainEntity"]["offers"]["itemOffered"][0]
        return subset_page_json

    @staticmethod
    def _is_product_page(soup):  # TODO: Implement this
        return True


def run():
    import argparse

    arg_parser = argparse.ArgumentParser(
        description="argument parser for Inflation Parser"
    )
    arg_parser.add_argument("--data-file-path", type=str)
    arg_parser.add_argument("--output-file-path", type=str)
    args = arg_parser.parse_args()
    logger.info(f"{args}")

    parsers = {"a101": A101Parser(), "migros": MigrosParser()}
    pm = ParserManager(parsers)

    dataset = pm.start_parsing(
        data_filepath=args.data_filepath,
        output_filepath=args.output_filepath,
        filename="deneme1.tsv",
    )
    print(dataset)


if __name__ == "__main__":
    run()
