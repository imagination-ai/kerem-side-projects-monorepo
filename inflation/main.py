from datetime import datetime
import logging
import os
import tempfile

from fastapi import BackgroundTasks, FastAPI

from common.clients.google_storage_client import get_storage_client
from common.customized_logging import configure_logging
from inflation.config import inflation_app_settings
from inflation.dataset.crawl import A101Crawler, CrawlerManager, MigrosCrawler
from inflation.dataset.parse import A101Parser, MigrosParser, ParserManager

CRAWLERS = {"a101": A101Crawler(), "migros": MigrosCrawler()}
PARSERS = {"a101": A101Parser(), "migros": MigrosParser()}

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
cm = CrawlerManager(CRAWLERS)
crawler_client = get_storage_client(inflation_app_settings.CRAWLER_BUCKET)
parser_client = get_storage_client(inflation_app_settings.PARSER_BUCKET)
pm = ParserManager(PARSERS)

OUTPUT_PATH_DIR = "/build/data"
CRAWLER_OUTPUT_DIR = f"{OUTPUT_PATH_DIR}/crawler"
PARSER_OUTPUT_DIR = f"{OUTPUT_PATH_DIR}/parser"

logger.info(
    f"Starting the application with -- Crawlers:{CRAWLERS}, Bucket Name:"
    f"{inflation_app_settings.CRAWLER_BUCKET}"
)
logger.info(
    f"Starting the application with -- Parsers:{PARSERS}, Bucket Name:"
    f"{inflation_app_settings.PARSER_BUCKET}"
)


def create_directory():
    dirs = [CRAWLER_OUTPUT_DIR, PARSER_OUTPUT_DIR]
    for directory in dirs:
        try:
            os.mkdir(directory)
            logger.info(f"{directory} is created")
        except OSError:
            logger.info(f"Skipping creating {directory} since it exists.")


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

    logger.info(
        f"Uploading {inflation_fn} to {inflation_app_settings.CRAWLER_BUCKET}/{basename}"
    )

    crawler_client.upload(inflation_fn, basename)
    logger.info(
        f"Crawling done for {excel_path}: {inflation_app_settings.CRAWLER_BUCKET}/"
        f"{basename}"
    )


def parse_inflation_data(source_filename, output_file_path, filename):
    logger.info(f"Parsing {source_filename} has been started.")
    _, suffix = os.path.splitext(source_filename)
    with tempfile.NamedTemporaryFile(suffix=suffix) as tmpfile:
        crawler_client.download(source_filename, tmpfile)
        tmpfile.flush()
        logger.info(f"Downloading {source_filename} done.")

        parsed_inflation_data_fn = pm.start_parsing(
            tmpfile.name, output_file_path, filename
        )
        logger.info(
            f"{source_filename} parsed successfully to {parsed_inflation_data_fn}."
        )

    basename = os.path.basename(parsed_inflation_data_fn)
    parser_client.upload(parsed_inflation_data_fn, basename)
    logger.info(
        f"Uploading {parsed_inflation_data_fn} InflationDataset obj to "  # not always
        # upload Inflation dataset. I should correct that.
        f"{inflation_app_settings.PARSER_BUCKET}/{basename}"
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


@app.on_event("startup")
async def startup_event():
    create_directory()


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
        "message": f"{inflation_app_settings.CRAWLER_BUCKET}/{filename} is preparing.",
        "data": {
            "bucket": inflation_app_settings.CRAWLER_BUCKET,
            "filename": filename,
        },
    }


@app.get("/Parse", tags=["Parse"])
async def parse_data(background_tasks: BackgroundTasks, source_filename):
    logger.info(f"Received parse request for {source_filename}")
    filename = f"{datetime.now().strftime('%Y-%m-%d')}.parse.tsv"
    background_tasks.add_task(
        parse_inflation_data, source_filename, PARSER_OUTPUT_DIR, filename
    )
    return {
        "success": True,
        "message": f"{inflation_app_settings.PARSER_BUCKET}/{source_filename} is "
        f"preparing. Output will be stored on"
        f"{filename}",
        "data": {
            "bucket": inflation_app_settings.PARSER_BUCKET,
            "filename": filename,
        },
    }


@app.get("/Stats", tags=["Stats"])
async def get_db_stats():
    return collect_db_stats(CRAWLER_OUTPUT_DIR)


if __name__ == "__main__":
    import uvicorn

    logger.warning("Friendly Warning: Local Development...")
    uvicorn.run(
        "inflation.main:app",
        host=inflation_app_settings.APP_HOST,
        port=inflation_app_settings.APP_PORT,
        reload=True,
        # reload_dirs='/tmp/',
        debug=True,
        workers=1,
    )
