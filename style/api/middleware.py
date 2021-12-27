import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


def add_middleware(app: FastAPI):
    @app.middleware("http")
    async def response_time_logger(request: Request, call_next):
        # Inbound: Customer - --> Server - --> Middleware --> Correct Endpoint
        # Outbound: Correct Endpoint --> Middleware --> Server --> Customer
        start_time = time.perf_counter()
        response = await call_next(request)
        total_time = time.perf_counter() - start_time
        logger.info(f"{request.method} {request.url.path} {total_time:.3}")
        return response
