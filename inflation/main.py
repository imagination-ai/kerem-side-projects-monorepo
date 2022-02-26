from datetime import datetime
import logging
import os

from fastapi import BackgroundTasks, FastAPI

from common.clients.google_storage_client import GoogleStorageClient
from common.customized_logging import configure_logging
from inflation.config import settings
from inflation.dataset.crawl import A101Crawler, CrawlerManager, MigrosCrawler

BUCKET_NAME = os.getenv("GCS_BUCKET", "inflation-in-turkey")

CRAWLERS = {"a101": A101Crawler(), "migros": MigrosCrawler()}

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
cm = CrawlerManager(CRAWLERS)
storage_client = GoogleStorageClient(bucket_name=BUCKET_NAME)

OUTPUT_PATH = "/applications/downloaded-files/"

logger.info(
    f"Starting the application with -- Crawlers:{CRAWLERS}, Bucket Name:{BUCKET_NAME}"
)


def fetch_inflation_data(excel_path, output_path, filename):
    """

    Args:
        excel_path: The path of spreadsheet file that contains products' information
        and their links.
        output_path: path of output json (inflation db)

    Returns:

    """
    logger.info(
        f"Crawling started with {excel_path} and output_path is {output_path} and "
        f"filename is {filename}"
    )
    records = cm.parse_excel_to_link_dataset(excel_path)
    inflation_fn = cm.start_crawling(records, output_path, filename)
    basename = os.path.basename(inflation_fn)

    logger.info(f"Uploading {inflation_fn} to {BUCKET_NAME}/{basename}")

    storage_client.upload(inflation_fn, basename)
    logger.info(f"Crawling done for {excel_path}: {BUCKET_NAME}/{basename}")


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
    excel_path="https://docs.google.com/spreadsheets/d"
    "/1Xv5UOTpzDPELdtk8JW1oDWbjpsEexAKKLzgzZBB-2vw/edit#gid=0",
):
    filename = f"{datetime.now().strftime('%Y-%m-%d')}.crawl.jsonl"
    background_tasks.add_task(
        fetch_inflation_data, excel_path, OUTPUT_PATH, filename
    )
    return {
        "success": True,
        "message": f"{BUCKET_NAME}/{filename} is preparing.",
    }


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
        reload=True,
        # reload_dirs='/tmp/',
        debug=True,
        workers=1,
    )
