import gzip
import json
from dataclasses import dataclass
import datetime

from bs4 import BeautifulSoup

NOT_AVAILABLE = "___NA___"


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
    in_stock: bool
    sample_date: datetime.datetime


class InflationDataset:
    def __init__(self, data: list):
        self.dataset = data

    def __len__(self):
        return len(self.dataset)

    def __iter__(self):
        return InflationDatasetIterator(self.dataset)

    # Q: boyle bir sey eklemeye gerek var mi?
    # def __str__(self):
    #     return str(self.dataset)

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


class InflationJSONA101DatasetReader(BaseJSONDataReader):
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
        if availability == "in stock":
            return True
        elif availability == "out of stock":
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
        with gzip.open(filename, "rt", encoding="UTF-8") as zipfile:
            total_pages = 0
            item_pages = 0
            for line in zipfile:
                line = json.loads(line)
                total_pages += 1

                # TODO: report how many lines are skipped.
                date = InflationJSONA101DatasetReader.__convert_sample_date(
                    line["timestamp"]
                )
                soup = BeautifulSoup(line["text"], "html.parser")
                if InflationJSONA101DatasetReader.__is_product_page(soup):
                    item_pages += 1
                    print(total_pages, item_pages)
                    record = InflationDataRecord(
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
        print(total_pages, item_pages)
        return InflationDataset(records)


def run():
    reader = InflationJSONA101DatasetReader()
    dataset = reader.read("a101.med.json.gz")
    # dataset = reader.read('a101.den.json.gz')
    # print(len(dataset))
    print(dataset)


if __name__ == "__main__":
    run()
