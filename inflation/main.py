from fastapi import FastAPI
import logging
import os
import json

from inflation.dataset.crawl import Crawler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
crawler = Crawler()


def fetch_inflation_data(excel_path, output_path):
    """

    Args:
        excel_path: The path of spreadsheet file that contains products' information and their links.
        output_path: path of output json (inflation db)

    Returns:

    """
    records = crawler.parse_excel_to_link_dataset(excel_path)
    crawler.crawl(records, output_path)


def collect_db_stats(db_path):
    """

    Args:
        db_path: DB Folder Path

    Returns: Dictionary (json file name: its length pairs)

    """
    db_stats = {}
    for entry in os.listdir(db_path):
        if os.path.isfile(os.path.join(db_path, entry)) and entry.endswith(
            ".json"
        ):
            with open(entry) as f:
                db_stats[entry] = len(json.load(f))

    return db_stats


@app.get("/crawl", tags=["crawl"])
async def fetch_data(
    excel_path="https://docs.google.com/spreadsheets/d/1mZSqW_X_KuQQdGhH7oAn3-MATyfePLlYYmOgE-mB_9Q/edit#gid=0",
    output_path="inflation-resources/data/db/",
):
    fetch_inflation_data(excel_path, output_path)
    return {"success": True, "message": "The data fetching is completed."}


@app.get("/stats", tags=["stats"])
async def get_db_stats(db_path="inflation-resources/data/db/"):
    return collect_db_stats(db_path)
