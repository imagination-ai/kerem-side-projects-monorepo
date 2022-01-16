import gzip
import json
from dataclasses import dataclass
from datetime import datetime

from bs4 import BeautifulSoup


class BaseJSONDataReader:
    def read(self, filename, columns=None):
        raise NotImplementedError()


@dataclass
class InflationDataRecord:
    product_name: str
    product_url: str
    product_code: str  # item identifier for this data.
    product_brand: str
    price: float
    currency: str
    stock: str
    sample_date: str  # Q: datetime.datetime niyeyse olmuyor? # price was valid for this date.


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


class InflationJSONDatasetReader(BaseJSONDataReader):
    @staticmethod
    def __get_product_name(soup):
        return soup.find("meta", property="og:title").attrs["content"]

    @staticmethod
    def __get_product_url(soup):
        return soup.find("meta", property="og:url").attrs["content"]

    @staticmethod
    def __get_product_code(soup):
        return (
            soup.find("div", {"class": "product-code"})
            .get_text()
            .split(": ")[1]
        )

    @staticmethod
    def __get_product_brand(soup):
        return soup.find("meta", property="og:brand").attrs["content"]

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
        return soup.find("meta", property="product:availability").attrs[
            "content"
        ]

    @staticmethod
    def __convert_sample_date(date: str):
        return datetime.strptime(date, "%Y%m%d%H%M%S")

    def read(self, filename, fields=None) -> InflationDataset:
        """It goes through the `filename` and create InflationRecords

        Args:
            filename:
            fields: fields to include. If it is None, include everything.

        Returns:

        """
        records = []
        with gzip.open(filename, "rt", encoding="UTF-8") as zipfile:
            for line in zipfile:
                line = json.loads(line)
                date = line["timestamp"]  # alttakini acinca silinecek
                # date = InflationJSONDatasetReader.__convert_sample_date(line['timestamp']) # Bunu dataclass'taki str type'ini datetime.datetime ile degistirince acacagim
                soup = BeautifulSoup(line["text"])
                record = InflationDataRecord(
                    InflationJSONDatasetReader.__get_product_name(soup),
                    InflationJSONDatasetReader.__get_product_url(soup),
                    InflationJSONDatasetReader.__get_product_code(soup),
                    InflationJSONDatasetReader.__get_product_brand(soup),
                    InflationJSONDatasetReader.__get_product_price(soup),
                    InflationJSONDatasetReader.__get_currency(soup),
                    InflationJSONDatasetReader.__item_in_stock(soup),
                    date,
                )
                records.append(record)

        return InflationDataset(records)
