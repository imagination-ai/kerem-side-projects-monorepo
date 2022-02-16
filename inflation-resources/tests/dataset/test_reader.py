import pytest
import datetime
from inflation.dataset.reader import (
    InflationJSONA101DatasetReader,
    InflationDataRecord,
)
from pathlib import Path

A101_TEST_SMALL_DATA_PATH = (
    Path(__file__).parents[2] / "tests/data/test_data_a101_small.json"
)


@pytest.fixture(scope="function")
def inflation_data_reader():
    return InflationJSONA101DatasetReader()


@pytest.fixture(scope="module")
def dataset():
    return InflationJSONA101DatasetReader().read(A101_TEST_SMALL_DATA_PATH)


def test_read_product(
    inflation_data_reader,
):
    record_data = inflation_data_reader.read(A101_TEST_SMALL_DATA_PATH)
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
