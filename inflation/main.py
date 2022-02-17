import logging
import os

from fastapi import BackgroundTasks, FastAPI

from common.customized_logging import configure_logging
from inflation.config import settings
from inflation.dataset.crawl import Crawler

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
crawler = Crawler()

OUTPUT_PATH = "/applications/downloaded-files/"


def fetch_inflation_data(excel_path, output_path):
    """

    Args:
        excel_path: The path of spreadsheet file that contains products' information
        and their links.
        output_path: path of output json (inflation db)

    Returns:

    """
    logger.info(
        f"Crawling started with {excel_path} and output_path is {output_path}"
    )
    records = crawler.parse_excel_to_link_dataset(excel_path)
    crawler.crawl(records, output_path)
    logger.info(f"Crawling done for {excel_path}")


def collect_db_stats(db_path):
    """

    Args:
        db_path: DB Folder Path

    Returns: Dictionary (json file name: its length pairs)

    """
    db_stats = {}
    for entry in os.listdir(db_path):
        entry = os.path.join(db_path, entry)
        if os.path.isfile(entry) and entry.endswith(".jsonl"):
            with open(entry) as f:
                db_stats[entry] = len(f.readlines())

    return db_stats


@app.get("/", tags=["Index"])
async def index():
    return {"success": True, "message": "Inflation Downloader is working!"}


@app.get("/Crawl", tags=["Crawl"])
async def fetch_data(
    background_tasks: BackgroundTasks,
    excel_path="https://docs.google.com/spreadsheets/d/1mZSqW_X_KuQQdGhH7oAn3"
    "-MATyfePLlYYmOgE-mB_9Q/edit#gid=0",
):
    background_tasks.add_task(fetch_inflation_data, excel_path, OUTPUT_PATH)
    return {"success": True, "message": "The data fetching started."}


@app.get("/Stats", tags=["Stats"])
async def get_db_stats():
    return collect_db_stats(OUTPUT_PATH)


if __name__ == "__main__":
    import uvicorn

    logger.warning("Friendly Warning: Local Development...")
    uvicorn.run(
        "inflation.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        # reload=True,
        # reload_dirs='/tmp/',
        debug=True,
        workers=1,
    )
