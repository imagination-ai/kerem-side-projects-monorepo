import pytest
import datetime
from pathlib import Path
import tempfile
import os

from inflation.dataset.reader import (
    A101Parser,
    InflationDataRecord,
)
from inflation.dataset.crawl import ItemRecord

INFLATION_RESOURCES_PATH = Path(__file__).parents[2]

TEST_FILE_PATHS = {
    "a101": "tests/data/test_data_a101_small.json",
    "migros": "NOTSPECIFIEDYET",
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


@pytest.fixture(scope="function")
def inflation_data_reader():
    return A101Parser()


@pytest.fixture(scope="module")
def a101_test_dataset():
    return A101Parser().parse(
        INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["a101"]
    )


@pytest.mark.xfail
def test_read_product(
    inflation_data_reader,
):
    record_data = inflation_data_reader.parse(
        INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["a101"]
    )
    truths = [
        InflationDataRecord(
            "0111101",
            "Pirinç",
            "A101",
            "Ovadan Pirinç Baldo 1000 G",
            "https://www.a101.com.tr/market/ovadan-pirinc-baldo-1000-g-1/",
            "14001902",
            "Ovadan",
            14.5,
            "TRY",
            True,
            datetime.datetime(2022, 2, 1, 22, 13, 23),
        ),
        InflationDataRecord(
            "0111201",
            "Buğday Unu",
            "A101",
            "Yeğenler Un Buğday 2 Kg",
            "https://www.a101.com.tr/market/yegenler-un-bugday-2-kg/",
            "28000285",
            "Yeğenler",
            15.9,
            "TRY",
            False,
            datetime.datetime(2022, 2, 1, 22, 13, 23),
        ),
        InflationDataRecord(
            "0111208",
            "Bebek Maması (Toz Karışım)",
            "A101",
            "Aptamil 2 Bebek Maması Biberon 1200 G",
            "https://www.a101.com.tr/anne-bebek-oyuncak/aptamil-2-bebek-mamasi-biberon-1200-g/",
            "17002483",
            "Aptamil",
            269.95,
            "TRY",
            True,
            datetime.datetime(2022, 2, 1, 22, 13, 23),
        ),
        InflationDataRecord(
            "0111209",
            "Bulgur",
            "A101",
            "Çiftçi Bulgur Pilavlık 2000 g",
            "https://www.a101.com.tr/market/ciftci-bulgur-pilavlik-2000-g/",
            "14000200",
            "Çiftçi",
            10.45,
            "TRY",
            False,
            datetime.datetime(2022, 2, 1, 22, 13, 24),
        ),
    ]

    for record, truth in zip(record_data, truths):
        assert record == truth


# TODO: I'll add this part after re-writing reader parser
@pytest.mark.xfail
def test_crawler_still_works_for_a101(crawler_manager):
    """
    It tests our crawler and reader still works on the A101 website.
    It's an online test it should fail time to time.

    Returns:

    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS_RND["a101"], tmpdirname, "test"
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        record_data = inflation_data_reader.read(test_data_fp)
        for record in record_data:
            assert record.item_code == "123"
            assert record.item_name == "pirinc"
            assert record.source == "a101"
            assert record.product_name == "Ovadan Pirinç Baldo 1000 G"
            assert record.product_code == "14001902"
            assert record.product_brand == "Ovadan"
            assert record.currency == "TRY"


# TODO: I'll add another test for migros
