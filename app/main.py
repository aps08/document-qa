import time

import uvicorn
from api.v1 import api_v1_router
from config import (
    config,
    custom_generic_exception,
    custom_http_exception,
    custom_validation_exception,
)
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils import logger

app = FastAPI(
    title="document-qa",
    version="0.1.0",
    description=config.DESCRIPTION,
    license_info={
        "name": "MIT License",
        "url": "https://github.com/aps08/document-qa/blob/main/LICENSE",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redocs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    start = time.time()
    logger.info(f"{request.method} {request.url.path} {request.headers['host']}")
    response = await call_next(request)
    processing_time = time.time() - start
    if processing_time > 10:
        logger.warning(f"Processing time longer than 10 seconds: {processing_time}")
    else:
        logger.info(f"Processing time:{processing_time}")
    return response


app.add_exception_handler(StarletteHTTPException, custom_http_exception)
app.add_exception_handler(RequestValidationError, custom_validation_exception)
app.add_exception_handler(Exception, custom_generic_exception)

app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
