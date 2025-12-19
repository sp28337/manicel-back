import logging
import time
from fastapi import Request

logger = logging.getLogger("http")


async def logging_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = round((time.perf_counter() - start_time) * 1000, 2)

    logger.info(
        "HTTP request",
        extra={
            "extra": {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration,
                "client": request.client.host if request.client else None,
            }
        },
    )

    return response
