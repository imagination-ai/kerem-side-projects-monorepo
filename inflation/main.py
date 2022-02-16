from fastapi import FastAPI
import logging
from inflation.dataset.crawl import Crawler


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
crawler = Crawler()


def fetch_inflation_data():
    url = "https://docs.google.com/spreadsheets/d/1mZSqW_X_KuQQdGhH7oAn3-MATyfePLlYYmOgE-mB_9Q/edit#gid=0"
    records = crawler.parse_excel_to_link_dataset(url)
    crawler.crawl(records, "/inflation-resources/data/")


@app.get("/crawl", tags=["crawl"])
async def fetch_data():
    fetch_inflation_data()
    return {"success": True, "message": "The data fetching is completed."}
