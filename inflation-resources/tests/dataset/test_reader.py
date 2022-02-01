import pytest
import datetime
from inflation.dataset.reader import (
    InflationJSONA101DatasetReader,
    InflationDataRecord,
)
from pathlib import Path


A101_TEST_DATA_PATH = (
    Path(__file__).parents[3]
    / "inflation-resources/tests/data/test_data_a101.json"
)

A101_TEST_SMALL_DATA_PATH = (
    Path(__file__).parents[3]
    / "inflation-resources/tests/data/test_data_a101_small.json"
)


@pytest.fixture(scope="function")
def inflation_data_reader():
    return InflationJSONA101DatasetReader()


@pytest.fixture(scope="module")
def dataset():
    return InflationJSONA101DatasetReader().read(A101_TEST_DATA_PATH)


def test_read_product(
    inflation_data_reader,
):
    record_data = inflation_data_reader.read(A101_TEST_DATA_PATH)
    truths = [
        InflationDataRecord(
            "Ahşap Ramazan Davulu",
            "https://www.a101.com.tr/anne-bebek/ahsap-ramazan-davulu/",
            "26017745",
            "",
            49.95,
            "TRY",
            True,
            datetime.datetime(2021, 11, 30, 0, 31, 22),
        ),
        InflationDataRecord(
            "Barbie Twistable Scooter 3 Tekerlekli",
            "https://www.a101.com.tr/anne-bebek/barbie-twistable-scooter-3-tekerlekli/",
            "26018419",
            "",
            129.95,
            "TRY",
            True,
            datetime.datetime(2021, 12, 4, 15, 51, 21),
        ),
    ]

    for record, truth in zip(record_data, truths):
        assert record == truth


def test_length_readable(dataset):
    """
    It controls the actual number of product pages that are read.
    """
    assert len(dataset) == 206
