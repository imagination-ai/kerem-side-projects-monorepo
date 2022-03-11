import logging

from common.customized_logging import configure_logging
from inflation.dataset.crawl import A101Crawler, CrawlerManager, MigrosCrawler
from inflation.dataset.parse import A101Parser, MigrosParser, ParserManager

configure_logging()
logger = logging.getLogger(__name__)


def run():
    import argparse

    parser = argparse.ArgumentParser(description="Crawl and Parse")
    parser.add_argument(
        "--excel-path",
        type=str,
        help="The file path or url of spreadsheet database file",
    )
    parser.add_argument(
        "--path", type=str, help="The name of the json record file"
    )

    args = parser.parse_args()
    logger.info(f"{args}")

    crawlers = {"a101": A101Crawler(), "migros": MigrosCrawler()}
    cm = CrawlerManager(crawlers)
    records = cm.parse_excel_to_link_dataset(file_path=args.excel_path)
    crawl_output_fn = cm.start_crawling(records, path=args.path)

    print(f"Crawling done. Data saved {crawl_output_fn}")

    # crawl_output_fn = "./inflation-crawl-20220302081502.jsonl.gz"
    # crawl_output_fn = "dataset/inflation-crawl-20220302074757.jsonl.gz"

    parsers = {"a101": A101Parser(), "migros": MigrosParser()}
    pm = ParserManager(parsers)
    parser_output_path = pm.start_parsing(crawl_output_fn, args.path)

    print(f"Parsing done. Data saved {parser_output_path}")


if __name__ == "__main__":
    run()
