import pytest
from inflation.dataset.crawl import Crawler

from pathlib import Path


TEST_LINK_EXCEL = (
    Path(__file__).parents[3] / "inflation-resources/tests/data/test_links.xlsx"
)


@pytest.fixture(scope="module")
def crawler():
    return Crawler()


@pytest.fixture(scope="module")
def records():
    return Crawler().parse_excel_to_link_dataset(TEST_LINK_EXCEL)


def test_crawl_parse_true_number(records):
    assert len(records) == 17


def test_crawl_parse_true_items(records):
    items_codes = []
    for record in records:
        items_codes.append(record.item_code)

    assert len(set(items_codes)) == 5


# Bu dogru yazma fonksiyonuyla ilgili de bir test lazim. Nasil yazmak lazim onu?
