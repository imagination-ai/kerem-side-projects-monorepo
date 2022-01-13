import logging
from inflation.dataset.common_crawl import CommonCrawlerDownloader
from common.customized_logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

url = "a101.com.tr/*"

downloader = CommonCrawlerDownloader()


def run():
    import argparse

    parser = argparse.ArgumentParser(description="download crawler data")
    parser.add_argument(
        "--url",
        default="json",
        nargs="?",
        choices=("json", "warc"),
        type=str,
        help="url of the web page",
    )
    parser.add_argument("--output-fn", type=str, help="target file")
    # choices Makefile #type , limit

    args = parser.parse_args()
    logger.info(f"{args}")

    if not any([args.url, args.output_fn]):
        logger.error("Either --url and --output-fn should be provided.")

    # if

    downloader.download_partially_as_json(
        url=args.url, output_fn=args.output_fn
    )
    # else:
    #     downloader.download_as_warc(
    #         url=url,
    #         warc_description="a101.com.tr/* dataset (run at Jan, 10 2022)",
    #         writer_prefix="a101-all",
    #         writer_subprefix="suffix",
    #         # limit=50,
    #     )


if __name__ == "__main__":
    run()
