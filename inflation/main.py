import tempfile
from datetime import datetime
import logging
import os
import gzip
import json

from fastapi import BackgroundTasks, FastAPI

from common.clients.google_storage_client import GoogleStorageClient
from common.customized_logging import configure_logging
from inflation.config import settings
from inflation.dataset.crawl import CrawlerManager, A101Crawler, MigrosCrawler
from inflation.dataset.parse import ParserManager, A101Parser, MigrosParser

CRAWLER_BUCKET = os.getenv("CRAWLER_BUCKET", "inflation-project-crawler-output")
PARSER_BUCKET = os.getenv("PARSER_BUCKET", "inflation-project-parser-output")

CRAWLERS = {"a101": A101Crawler(), "migros": MigrosCrawler()}
PARSERS = {"a101": A101Parser(), "migros": MigrosParser()}

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
cm = CrawlerManager(CRAWLERS)
crawler_client = GoogleStorageClient(bucket_name=CRAWLER_BUCKET)
parser_client = GoogleStorageClient(bucket_name=PARSER_BUCKET)
pm = ParserManager(PARSERS)

OUTPUT_PATH_DIR = (
    "/build/data"  # Q: Eger build diye verirsek bunu local'de nasil calisacak?
)
CRAWLER_OUTPUT_DIR = f"{OUTPUT_PATH_DIR}/crawler"
PARSER_OUTPUT_DIR = f"{OUTPUT_PATH_DIR}/parser"

logger.info(
    f"Starting the application with -- Crawlers:{CRAWLERS}, Bucket Name:{CRAWLER_BUCKET}"
)
logger.info(
    f"Starting the application with -- Parsers:{PARSERS}, Bucket Name:{PARSER_BUCKET}"
)


def create_directory():
    dirs = [CRAWLER_OUTPUT_DIR, PARSER_OUTPUT_DIR]
    for directory in dirs:
        try:
            os.mkdir(directory)
            logger.info(f"{directory} is created")
        except OSError:
            logger.info(f"Skipping creating {directory} since it exists.")


create_directory()


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

    logger.info(f"Uploading {inflation_fn} to {CRAWLER_BUCKET}/{basename}")

    crawler_client.upload(inflation_fn, basename)
    logger.info(f"Crawling done for {excel_path}: {CRAWLER_BUCKET}/{basename}")


def parse_inflation_data(source_filename, output_file_path, filename):
    _, suffix = os.path.splitext(source_filename)
    with tempfile.NamedTemporaryFile(suffix=suffix) as tmpfile:
        crawler_client.download(source_filename, tmpfile)
        tmpfile.flush()

        parsed_inflation_data_fn = pm.start_parsing(
            tmpfile.name, output_file_path, filename
        )
        logger.info(
            f"{source_filename} parsed successfully to {parsed_inflation_data_fn}."
        )

    basename = os.path.basename(parsed_inflation_data_fn)
    parser_client.upload(parsed_inflation_data_fn, basename)
    logger.info(
        f"Uploading {parsed_inflation_data_fn} InflationDataset object to "
        f"{PARSER_BUCKET}/{basename}"
    )


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
async def fetch_data_async(
    background_tasks: BackgroundTasks,
    excel_path="https://docs.google.com/spreadsheets/d"
    "/1Xv5UOTpzDPELdtk8JW1oDWbjpsEexAKKLzgzZBB-2vw/edit#gid=0",
):
    filename = f"{datetime.now().strftime('%Y-%m-%d')}.crawl.jsonl.gz"
    background_tasks.add_task(
        fetch_inflation_data, excel_path, CRAWLER_OUTPUT_DIR, filename
    )
    return {
        "success": True,
        "message": f"{CRAWLER_BUCKET}/{filename} is preparing.",
        "data": {"bucket": CRAWLER_BUCKET, "filename": filename},
    }


@app.get("/Parse", tags=["Parse"])
async def parse_data(background_tasks: BackgroundTasks, source_filename):
    filename = f"{datetime.now().strftime('%Y-%m-%d')}.parse.jsonl.gz"
    background_tasks.add_task(
        parse_inflation_data, source_filename, PARSER_OUTPUT_DIR, filename
    )
    return {
        "success": True,
        "message": f"{PARSER_BUCKET}/{source_filename} is preparing. Output will be "
        f"{filename}",
        "data": {"bucket": PARSER_BUCKET, "filename": filename},
    }


@app.get("/Stats", tags=["Stats"])
async def get_db_stats():
    return collect_db_stats(CRAWLER_OUTPUT_DIR)


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
