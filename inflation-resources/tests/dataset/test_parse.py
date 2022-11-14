import numpy as np
import pandas as pd
import pytest
import datetime
from pathlib import Path
import tempfile
import os


from inflation.dataset.parse import (
    ParserManager,
    InflationDataRecord,
    InflationDataset,
    A101Parser,
    MigrosParser,
    MacroCenterParser,
)
from inflation.dataset.crawl import (
    ItemRecord,
    CrawlerManager,
    A101Crawler,
    MigrosCrawler,
    MacroCenterCrawler,
)

INFLATION_RESOURCES_PATH = Path(__file__).parents[2]
DTYPE_DIC = {"item_code": str}
TEST_FILE_PATHS = {
    "a101": "tests/data/test_data_a101_small.jsonl.gz",
    "migros": "tests/data/test_data_migros.small.jsonl.gz",
}

CRAWLERS = {
    "a101": A101Crawler(),
    "migros": MigrosCrawler(),
    "macrocenter": MacroCenterCrawler(),
}
PARSERS = {
    "a101": A101Parser(),
    "migros": MigrosParser(),
    "macrocenter": MacroCenterParser(),
}

RECORDS_FOR_ONLINE_TRIALS = {
    "a101": [
        ItemRecord(
            "0111101",
            "pirinc",
            "ovadan",
            "https://www.a101.com.tr/market/ovadan-pirinc-baldo-1000-g-1",
            "a101",
        )
    ],
    "migros": [
        ItemRecord(
            "0114101",
            "sut",
            "pinar",
            "https://www.migros.com.tr/pinar-organik-sut-1-l-p-a822f9",
            "migros",
        )
    ],
    "macrocenter": [
        ItemRecord(
            "0111209",
            "bulgur",
            "duru",
            "https://www.macrocenter.com.tr/duru-pilavlik-bulgur-1000-g-p-106755",
            "macrocenter",
        )
    ],
}


@pytest.fixture(scope="module")
def parser_manager():
    return ParserManager(PARSERS)


@pytest.fixture(scope="module")
def crawler_manager():
    return CrawlerManager(CRAWLERS)


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

    for input_format in ("tsv", "pickle"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            parsed_data_fp = parser_manager.start_parsing(
                str(INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["a101"]),
                tmpdirname,
                "sample-filename.json.gz",
                output_format=input_format,
            )

            parsed_dataset = InflationDataset.read(
                parsed_data_fp, input_format=input_format
            )
            for data_record, truth in zip(parsed_dataset, truths):
                assert data_record == truth


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
            "01012801",
            "Yayla",
            24.22,
            "TRY",
            True,
            datetime.datetime(2022, 3, 3, 14, 20, 15),
        ),
        InflationDataRecord(
            "0111201",
            "Buğday Unu",
            "migros",
            "Söke Tam Buğday Unu 1 Kg",
            "https://www.migros.com.tr/soke-tam-bugday-unu-1-kg-p-4c73f6",
            "05010422",
            "Söke",
            18.5,
            "TRY",
            True,
            datetime.datetime(2022, 3, 3, 14, 20, 17),
        ),
        InflationDataRecord(
            "0111208",
            "Bebek Maması (Toz Karışım)",
            "migros",
            "Bebelac Devam Sütü 1 400 G",
            "https://www.migros.com.tr/bebelac-devam-sutu-1-400-g-p-4cec83",
            "05041283",
            "Bebelac",
            69.95,
            "TRY",
            True,
            datetime.datetime(2022, 3, 3, 14, 20, 19),
        ),
        InflationDataRecord(
            "0111209",
            "Bulgur",
            "migros",
            "Yayla Pilavlık Bulgur 1 Kg",
            "https://www.migros.com.tr/yayla-pilavlik-bulgur-1-kg-p-1057a6",
            "01071014",
            "Yayla",
            15.8,
            "TRY",
            True,
            datetime.datetime(2022, 3, 3, 14, 20, 20),
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdirname:
        parsed_data_fp = parser_manager.start_parsing(
            str(INFLATION_RESOURCES_PATH / TEST_FILE_PATHS["migros"]),
            tmpdirname,
            "sample-filename.json.gz",
        )

        parsed_dataset = InflationDataset.read(parsed_data_fp)
        for data_record, truth in zip(parsed_dataset, truths):
            assert data_record == truth


# @pytest.mark.skip
def test_online_a101_crawler(crawler_manager, parser_manager):
    """
    It tests our crawler and reader still works on the A101 website.
    It's an online test it should fail time to time.

    Returns:

    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS_FOR_ONLINE_TRIALS["a101"],
            tmpdirname,
            "a101-test.jsonl.gz",
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        record_data_path = parser_manager.start_parsing(
            test_data_fp, tmpdirname, "a101-test.tsv"
        )
        record = pd.read_csv(record_data_path, sep="\t", dtype=DTYPE_DIC)
        assert record.item_code[0] == "0111101"
        assert record.item_name[0] == "pirinc"
        assert record.source[0] == "a101"
        assert record.product_name[0] == "Ovadan Pirinç Baldo 1000 G"
        assert record.product_code[0] == 14001902
        assert record.product_brand[0] == "Ovadan"
        assert record.currency[0] == "TRY"
        assert type(record.price[0]) is np.float64


# @pytest.mark.skip
def test_online_migros_crawler(crawler_manager, parser_manager):
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS_FOR_ONLINE_TRIALS["migros"],
            tmpdirname,
            "migros-test.jsonl.gz",
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        record_data_path = parser_manager.start_parsing(
            test_data_fp, tmpdirname, "migros-test.tsv"
        )
        record = pd.read_csv(record_data_path, sep="\t", dtype=DTYPE_DIC)
        assert record.item_code[0] == "0114101"
        assert record.item_name[0] == "sut"
        assert record.source[0] == "migros"
        assert record.product_name[0] == "Pınar Organik Süt 1 L"
        assert record.product_code[0] == 11019001
        assert record.product_brand[0] == "Pınar"
        assert record.currency[0] == "TRY"
        assert type(record.price[0]) is np.float64


# @pytest.mark.skip
def test_online_macrocenter_crawler(crawler_manager, parser_manager):
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_data_fp = crawler_manager.start_crawling(
            RECORDS_FOR_ONLINE_TRIALS["macrocenter"],
            tmpdirname,
            "macro-test.jsonl.gz",
        )
        files = []
        for entry in os.listdir(tmpdirname):
            if os.path.isfile(os.path.join(tmpdirname, entry)):
                files.append(entry)
        assert len(files) == 1
        record_data_path = parser_manager.start_parsing(
            test_data_fp,
            tmpdirname,
            "macro-test.tsv",
        )
        record = pd.read_csv(record_data_path, sep="\t", dtype=DTYPE_DIC)
        assert record.item_code[0] == "0111209"
        assert record.item_name[0] == "bulgur"
        assert record.source[0] == "macrocenter"
        assert record.product_name[0] == "Duru Pilavlik Bulgur 1000 G"
        assert np.isnan(record.product_code[0])
        assert record.product_brand[0] == "Duru Bulgur"
        assert record.currency[0] == "TRY"
        assert type(record.price[0]) is np.float64
