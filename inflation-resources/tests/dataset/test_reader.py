import pytest
import datetime
from inflation.dataset.reader import InflationJSONA101DatasetReader
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
    results = [
        [
            "Ahşap Ramazan Davulu",
            "https://www.a101.com.tr/anne-bebek/ahsap-ramazan-davulu/",
            "26017745",
            "",
            49.95,
            "TRY",
            True,
            datetime.datetime(2021, 11, 30, 0, 31, 22),
        ],
        [
            "Barbie Twistable Scooter 3 Tekerlekli",
            "https://www.a101.com.tr/anne-bebek/barbie-twistable-scooter-3-tekerlekli/",
            "26018419",
            "",
            129.95,
            "TRY",
            True,
            datetime.datetime(2021, 12, 4, 15, 51, 21),
        ],
    ]
    for record, result in zip(record_data, results):
        assert record.product_name == result[0]
        assert record.product_url == result[1]
        assert record.product_code == result[2]
        assert record.product_brand == result[3]
        assert record.price == result[4]
        assert record.currency == result[5]
        assert record.in_stock == result[6]
        assert record.sample_date == result[7]
