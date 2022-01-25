import pandas as pd
from pathlib import Path
from dataclasses import dataclass

LINKS_FILE_PATH = (
    Path(__file__).parents[2] / "inflation-resources/data/links.xlsx"
)


@dataclass
class TurkstatDataRecord:
    turkstat_item_code: str
    turkstat_item_name: str
    product_names_and_links: dict


f = pd.ExcelFile(LINKS_FILE_PATH)
df = f.parse(f.sheet_names[0])


class LinkDataset:
    def __init__(
        self, data: list
    ):  # Q: Reader'da da burada da RecordClassi oldugunu yazmak daha dogru olmaz mi?
        self.dataset = data

    def __len__(self):
        return len(self.dataset)

    def __iter__(self):
        NotImplementedError


def run():
    pass


if __name__ == "__main__":
    run()
