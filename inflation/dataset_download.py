import datetime
import logging
from inflation.dataset.common_crawl import CommonCrawlerDownloader
from common.customized_logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

downloader = CommonCrawlerDownloader()


def run():
    import argparse

    parser = argparse.ArgumentParser(description="download crawler data")
    parser.add_argument("--url", type=str, help="url of the web page")
    parser.add_argument("--output-fn", type=str, help="target file")
    parser.add_argument(
        "--type",
        type=str,
        choices=("json", "warc"),
        help="file type of the target file",
    )
    parser.add_argument("--limit", type=int, help="limit the download")

    args = parser.parse_args()
    logger.info(f"{args}")

    if args.type == "json":
        downloader.download_partially_as_json(
            url=args.url, output_fn=args.output_fn, limit=args.limit
        )
    else:
        downloader.download_as_warc(
            url=args.url,
            warc_description=f"{args.url} dataset (run at {datetime.datetime.now()})",
            writer_prefix="data",
            writer_subprefix="",
            limit=args.limit,
        )


if __name__ == "__main__":
    run()
