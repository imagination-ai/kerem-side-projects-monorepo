import requests
import json
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

LINKS_FILE_PATH = (
    Path(__file__).parents[2] / "inflation-resources/data/links.xlsx"
)


@dataclass
class TurkstatItemRecord:
    turkstat_item_code: str
    turkstat_item_name: str
    product_name: str
    product_url: str


class LinkDataset:
    def __init__(
        self, data: list
    ):  # Q: Reader'da da burada da RecordClassi oldugunu yazmak daha dogru olmaz mi?
        self.dataset = data

    def __len__(self):
        return len(self.dataset)

    def __iter__(self):
        NotImplementedError


def parse_link_item_dataset(file_path):
    """It takes excel file path convert them into TurkstatDatarecord class and save it into a list.
    It returns LinkDataset class.
    Note: Only works with the first sheet of an Excel file.
    """

    records = []

    excel_file = pd.ExcelFile(file_path)
    df = excel_file.parse(excel_file.sheet_names[0])

    for row in df.iterrows():
        item_code = row[1][0]
        item_name = row[1][1]
        product_name = row[1][2]
        link = row[1][3]

        record = TurkstatItemRecord(item_code, item_name, product_name, link)
        records.append(record)

    return records


def crawl(records: LinkDataset):
    """ """

    for record in records:

        r = requests.get(record.product_url)

        now = datetime.now()
        date = now.strftime("%Y%m%d%H%M%S")

        d = {
            "text": r.text,
            "timestamp": date,
            "turkstat_item_code": record.turkstat_item_code,
            "product_name": record.product_name,
        }

        with open("a101.json", "a") as file:
            json.dump(d, file)
            file.write("\n")


def run():
    records = parse_link_item_dataset(LINKS_FILE_PATH)
    crawl(records)


if __name__ == "__main__":
    run()
