from inflation.dataset.common_crawl import CommonCrawlerDownloader

# TODO (Kerem): Make this part parametric with argparse. See examples from other projects.

url = "a101.com.tr/*"


downloader = CommonCrawlerDownloader()
# downloader.download_as_warc(
#     url=url,
#     warc_description="a101.com.tr/* dataset (run at Jan, 10 2022)",
#     writer_prefix="a101-all",
#     writer_subprefix="suffix",
#     # limit=50,
# )

downloader.download_partially_as_json(
    url=url,
    output_fn="a101.json.gz",
    # limit=50,
)
