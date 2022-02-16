import json

import pytest
import tempfile
import os
from unittest import mock
from pathlib import Path
from inflation.dataset.crawl import Crawler
from inflation.dataset.crawl import ItemRecord
from inflation.dataset.reader import InflationJSONA101DatasetReader


TEST_LINK_EXCEL = Path(__file__).parents[2] / "tests/data/test_links.xlsx"

TEST_PAGE = (
    Path(__file__).parents[2]
    / "tests/data/pages/ovadan-pirinc-baldo-1000-g-a101.html"
)

RECORDS = [
    ItemRecord("123", "pirinc", "ovadan", "http://www.gmail.com", "A101")
]

RECORDS_RND = [
    ItemRecord(
        "123",
        "pirinc",
        "ovadan",
        "https://www.a101.com.tr/market/ovadan-pirinc-baldo-1000-g-1",
        "A101",
    )
]


@pytest.fixture(scope="module")
def inflation_data_reader():
    return InflationJSONA101DatasetReader()


@pytest.fixture(scope="module")
def html_test_file():
    import codecs

    return codecs.open(TEST_PAGE, "r").read()


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


@mock.patch("inflation.dataset.crawl.requests.get")
def test_crawl_output(mock_requests_get, crawler, html_test_file):
    """
    (1) It tests the Crawler's crawl method creates output file (a json).
    (2) It tests this file exist or not.
    """

    mock_requests_get.return_value = mock.Mock(
        status_code=200, text=html_test_file
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        fn = tmpdirname + "/" + "test"
        crawler.crawl(RECORDS, fn)
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        test_data_fp = tmpdirname + "/" + files[0]
        f = open(test_data_fp)
        test_data = json.load(f)
        assert test_data["item_code"] == "123"
        assert test_data["item_name"] == "pirinc"
        assert test_data["product_name"] == "ovadan"
        assert test_data["source"] == "A101"
        assert len(test_data["text"]) == 282375


def test_crawl_and_read_A101(crawler, inflation_data_reader):
    """
    It tests our crawler and reader still works on the A101 website.
    Args:
        crawler:

    Returns:

    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        fn = tmpdirname + "/" + "test"
        crawler.crawl(RECORDS_RND, fn)
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        test_data_fp = tmpdirname + "/" + files[0]
        record_data = inflation_data_reader.read(test_data_fp)
        for record in record_data:
            assert record.item_code == "123"
            assert record.item_name == "pirinc"
            assert record.source == "A101"
            assert record.product_name == "Ovadan Pirinç Baldo 1000 G"
            assert record.product_code == "14001902"
            assert record.product_brand == "Ovadan"
            assert record.currency == "TRY"
