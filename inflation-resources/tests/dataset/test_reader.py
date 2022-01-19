from collections import namedtuple

import pytest
import datetime
from inflation.dataset.reader import (
    InflationJSONA101DatasetReader,
    InflationDataRecord,
)
from pathlib import Path

PRODUCT_PAGE_DATA_PATH = (
    Path(__file__).parents[3]
    / "inflation-resources/tests/data/product_page.json.gz"
)


@pytest.fixture(scope="function")
def inflation_data_reader():
    return InflationJSONA101DatasetReader()


def test_read_product(
    inflation_data_reader,
):  # Q: 3 tane yok muydu niye 2 tane geldi?
    record_data = inflation_data_reader.read(PRODUCT_PAGE_DATA_PATH)
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
