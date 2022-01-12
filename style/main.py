from fastapi import FastAPI
import logging
from starlette.middleware.cors import CORSMiddleware

from style.api.middleware import add_middleware
from style.api.routers import prediction
from style.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
add_middleware(app)

origins = ["http://localhost:3000", "https://blog.kerem.baskaya.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.get("/", tags=["Index"])
async def index():
    return {"success": True, "message": "Style Predictor is working!"}


app.include_router(
    prediction.router,
    prefix=settings.API_BASE_URL
    + "/Predictions",  # http://.../api/v1/Predictions/
    tags=["Predictions Router"],
)

if __name__ == "__main__":
    import uvicorn

    logger.warning("Friendly Warning: Local Development...")
    uvicorn.run(
        "style.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        debug=True,
        workers=1,
    )
