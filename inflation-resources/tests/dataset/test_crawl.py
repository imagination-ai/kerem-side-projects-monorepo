import pytest
import tempfile
import os
from unittest import mock
from pathlib import Path
from inflation.dataset.crawl import Crawler
from inflation.dataset.crawl import ItemRecord

TEST_LINK_EXCEL = (
    Path(__file__).parents[3] / "inflation-resources/tests/data/test_links.xlsx"
)

TEST_PAGE = (
    Path(__file__).parents[3]
    / "inflation-resources/tests/data/pages/Ovadan-Pirinç-Baldo-1000-G-A101.html"
)

rec = [ItemRecord("123", "pirinc", "ovadan", "http://www.gmail.com", "A101")]


@pytest.fixture(scope="function")
def html_test_file():
    import codecs

    f = codecs.open(TEST_PAGE, "r").read()
    return f


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
        crawler.crawl(rec, fn)
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        print(files)
        assert len(files) == 1
