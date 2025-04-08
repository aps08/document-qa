import uvicorn
from api.v1 import api_v1_router
from config.exceptions import (custom_generic_exception, custom_http_exception,
                               custom_validation_exception)
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="document-qa",
    version="0.0.1",
    # description=config.DESCRIPTION,
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
    # allow_origins=config.ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, custom_http_exception)
app.add_exception_handler(RequestValidationError, custom_validation_exception)
app.add_exception_handler(Exception, custom_generic_exception)

app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
