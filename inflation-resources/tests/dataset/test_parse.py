import pytest
import datetime
from pathlib import Path
import tempfile
import os

from inflation.dataset.parse import (
    ParserManager,
    InflationDataRecord,
    A101Parser,
    MigrosParser,
)
from inflation.dataset.crawl import (
    ItemRecord,
    CrawlerManager,
    A101Crawler,
    MigrosCrawler,
)

INFLATION_RESOURCES_PATH = Path(__file__).parents[2]

TEST_FILE_PATHS = {
    "a101": "tests/data/test_data_a101_small.jsonl.gz",
    "migros": "tests/data/test_data_migros.small.jsonl.gz",
}

CRAWLERS = {"a101": A101Crawler(), "migros": MigrosCrawler()}

PARSERS = {"a101": A101Parser(), "migros": MigrosParser()}

RECORDS_FOR_ONLINE_TRIALS = {
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
def parser_manager():
    return ParserManager(PARSERS)


@pytest.fixture(scope="module")
def crawler_manager():
    return CrawlerManager(CRAWLERS)


# @pytest.fixture(scope="module")
# def a101_test_dataset():
#     return ParserManager(PARSERS).parse(
#         INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["a101"]
#     )


@pytest.mark.skip
def test_a101_parse_product(
    parser_manager,
):

    truths = [
        InflationDataRecord(
            "0111101",
            "Pirinç",
            "a101",
            "Ovadan Pirinç Baldo 1000 G",
            "https://www.a101.com.tr/market/ovadan-pirinc-baldo-1000-g-1/",
            "14001902",
            "Ovadan",
            13.5,
            "TRY",
            True,
            datetime.datetime(2022, 3, 1, 19, 27, 59),
        ),
        InflationDataRecord(
            "0111201",
            "Buğday Unu",
            "a101",
            "Yeğenler Un Buğday 2 Kg",
            "https://www.a101.com.tr/market/yegenler-un-bugday-2-kg/",
            "28000285",
            "Yeğenler",
            15.9,
            "TRY",
            False,
            datetime.datetime(2022, 3, 1, 19, 27, 59),
        ),
        InflationDataRecord(
            "0111208",
            "Bebek Maması (Toz Karışım)",
            "a101",
            "Aptamil 2 Bebek Maması Biberon 1200 G",
            "https://www.a101.com.tr/anne-bebek-oyuncak/aptamil-2-bebek-mamasi-biberon-1200-g/",
            "17002483",
            "Aptamil",
            252.5,
            "TRY",
            True,
            datetime.datetime(2022, 3, 1, 19, 27, 59),
        ),
        InflationDataRecord(
            "0111209",
            "Bulgur",
            "a101",
            "Çiftçi Bulgur Pilavlık 2000 g",
            "https://www.a101.com.tr/market/ciftci-bulgur-pilavlik-2000-g/",
            "14000200",
            "Çiftçi",
            10.45,
            "TRY",
            False,
            datetime.datetime(2022, 3, 1, 19, 28),
        ),
    ]

    record_data = parser_manager.start_parsing_from_drive(
        str(INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["a101"])
    )
    for record, truth in zip(record_data, truths):
        assert record == truth


@pytest.mark.skip
def test_migros_parse_products(
    parser_manager,
):
    truths = [
        InflationDataRecord(
            "0111101",
            "Pirinç",
            "migros",
            "Yayla Baldo Pirinç 1 Kg Gönen Bölgesi Mahsulü",
            "https://www.migros.com.tr/yayla-baldo-pirinc-1-kg-gonen-bolgesi-mahsulu-p-f7441",
            "14001902",
            "Yayla",
            24.22,
            "TRY",
            True,
            datetime.datetime(2022, 3, 1, 19, 27, 59),
        ),
        InflationDataRecord(
            "0111201",
            "Buğday Unu",
            "migros",
            "Söke Tam Buğday Unu 1 Kg",
            "https://www.migros.com.tr/soke-tam-bugday-unu-1-kg-p-4c73f6",
            "28000285",
            "Söke",
            18.5,
            "TRY",
            False,
            datetime.datetime(2022, 3, 1, 19, 27, 59),
        ),
        InflationDataRecord(
            "0111208",
            "Bebek Maması (Toz Karışım)",
            "migros",
            "Bebelac Devam Sütü 1 400 G",
            "https://www.migros.com.tr/bebelac-devam-sutu-1-400-g-p-4cec83",
            "17002483",
            "Bebelac",
            72.85,
            "TRY",
            True,
            datetime.datetime(2022, 3, 1, 19, 27, 59),
        ),
        InflationDataRecord(
            "0111209",
            "Bulgur",
            "migros",
            "Yayla Pilavlık Bulgur 1 Kg",
            "https://www.migros.com.tr/yayla-pilavlik-bulgur-1-kg-p-1057a6",
            "14000200",
            "Yayla",
            10.45,
            "TRY",
            False,
            datetime.datetime(2022, 3, 1, 19, 28),
        ),
    ]

    record_data = parser_manager.start_parsing_from_drive(
        str(INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["migros"])
    )
    for record, truth in zip(record_data, truths):
        assert record == truth


@pytest.mark.skip
def test_online_a101_crawler(crawler_manager, parser_manager):
    """
    It tests our crawler and reader still works on the A101 website.
    It's an online test it should fail time to time.

    Returns:

    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS_FOR_ONLINE_TRIALS["a101"], tmpdirname, "test"
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        record_data = parser_manager.start_parsing_from_drive(test_data_fp)
        for record in record_data:
            assert record.item_code == "123"
            assert record.item_name == "pirinc"
            assert record.source == "a101"
            assert record.product_name == "Ovadan Pirinç Baldo 1000 G"
            assert record.product_code == "14001902"
            assert record.product_brand == "Ovadan"
            assert record.currency == "TRY"
