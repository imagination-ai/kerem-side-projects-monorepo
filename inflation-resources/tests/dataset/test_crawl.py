import json

import pytest
import tempfile
import os
from unittest import mock
from pathlib import Path
from inflation.dataset.crawl import CrawlerManager
from inflation.dataset.crawl import ItemRecord
from inflation.dataset.reader import InflationJSONA101DatasetReader
from inflation.dataset.crawl import A101Crawler
from inflation.dataset.crawl import MigrosCrawler

CRAWLERS = {"a101": A101Crawler(), "migros": MigrosCrawler()}

INFLATION_RESOURCES_PATH = Path(__file__).parents[2]

TEST_PAGES_PATH = {
    "a101": "tests/data/pages/ovadan-pirinc-baldo-1000-g-a101.html",
    "migros": "tests/data/pages/pinar-organik-sut-1L-migros.html",
}

RECORDS = {
    "a101": [
        ItemRecord("123", "pirinc", "ovadan", "http://www.a101.com", "a101")
    ],
    "a101-mig": [
        ItemRecord("505", "sut", "pinar", "http://www.a101.com", "a101")
    ],
}

RECORDS_RND = {
    "a101": [
        ItemRecord(
            "123",
            "pirinc",
            "ovadan",
            "https://www.a101.com.tr/market/ovadan-pirinc-baldo-1000-g-1",
            "a101",
        )
    ],
    "migros": [
        ItemRecord(
            "505",
            "sut",
            "pinar",
            "https://www.migros.com.tr/pinar-organik-sut-1-l-p-a822f9",
            "migros",
        )
    ],
}


@pytest.fixture(scope="module")
def inflation_data_reader():
    return InflationJSONA101DatasetReader()


@pytest.fixture(scope="module")
def html_test_file_for_a101():
    import codecs

    return codecs.open(
        INFLATION_RESOURCES_PATH / TEST_PAGES_PATH["a101"], "r"
    ).read()


@pytest.fixture(scope="module")
def html_test_file_for_migros():
    import codecs

    return codecs.open(
        INFLATION_RESOURCES_PATH / TEST_PAGES_PATH["migros"], "r"
    ).read()


@pytest.fixture(scope="module")
def crawler_manager():
    return CrawlerManager(CRAWLERS)


@pytest.fixture(scope="module")
def records():
    fp = (
        INFLATION_RESOURCES_PATH / "tests/data/test_links.xlsx"
    )  # test links excel file path
    return CrawlerManager(CRAWLERS).parse_excel_to_link_dataset(fp)


def test_crawl_parse_true_number(records):
    assert len(records) == 17


def test_crawl_parse_true_items(records):
    items_codes = []
    for record in records:
        items_codes.append(record.item_code)

    assert len(set(items_codes)) == 5


@mock.patch("inflation.dataset.crawl.requests.get")
def test_start_crawling_check_output_for_a101(
    mock_requests_get, crawler_manager, html_test_file_for_a101
):
    """
    (1) It tests the Crawler's start crawling method using A101 case, creates output file (a json).
    (2) It tests this file exist or not.
    """

    mock_requests_get.return_value = mock.Mock(
        status_code=200, text=html_test_file_for_a101
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS["a101"], tmpdirname
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        f = open(test_data_fp)
        test_data = json.load(f)
        assert test_data["item_code"] == "123"
        assert test_data["item_name"] == "pirinc"
        assert test_data["product_name"] == "ovadan"
        assert test_data["source"] == "a101"
        assert (
            len(test_data["text"]) == 31721
        )  # TODO: (KEREM) validate if this is correct.


@mock.patch("inflation.dataset.crawl.requests.get")
def test_start_crawling_check_output_for_migros(
    mock_requests_get, crawler_manager, html_test_file_for_migros
):
    """
    (1) It tests the Crawler's start crawling method using Migros case, creates output file (a json).
    (2) It tests this file exist or not.
    """

    mock_requests_get.return_value = mock.Mock(
        status_code=200,
        text=html_test_file_for_migros,  # TODO: I must change mock part since this use selenium
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS["a101-mig"], tmpdirname
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        f = open(test_data_fp)
        test_data = json.load(f)
        assert test_data["item_code"] == "505"
        assert test_data["item_name"] == "sut"
        assert test_data["product_name"] == "pinar"
        assert test_data["source"] == "a101"
        assert (
            len(test_data["text"]) == 6561
        )  # TODO(KEREM) validate if this is correct.


# TODO: I'll add this part after re-writing reader parser
# def test_crawler_still_works_for_a101(crawler_manager):
#     """
#     It tests our crawler and reader still works on the A101 website.
#     It's an online test it should fail time to time.
#
#     Returns:
#
#     """
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         test_data_fp = crawler_manager.start_crawling(RECORDS_RND['a101'], tmpdirname, "test")
#         files = []
#         for entry in os.listdir(tmpdirname):
#             if os.path.isfile(os.path.join(tmpdirname, entry)):
#                 files.append(entry)
#         assert len(files) == 1
#         record_data = inflation_data_reader.read(test_data_fp)
#         for record in record_data:
#             assert record.item_code == "123"
#             assert record.item_name == "pirinc"
#             assert record.source == "a101"
#             assert record.product_name == "Ovadan Pirinç Baldo 1000 G"
#             assert record.product_code == "14001902"
#             assert record.product_brand == "Ovadan"
#             assert record.currency == "TRY"

# TODO: I'll add another test for migros
