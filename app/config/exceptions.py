"""
This module contains custom exception handlers for the FastAPI application.
Each function is designed to handle specific types of exceptions and return
a standardized response format.
"""

from config.response import Response
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils import logger


def custom_http_exception(request: Request, exc: StarletteHTTPException) -> Response:
    """
    Handles HTTP exceptions and returns a standardized response.

    Args:
        exc (HTTPException): The exception instance.
        request (Optional[Request]): The HTTP request object (default is None).

    Returns:
        Response: A standardized HTTP response with the exception details.
    """
    logger.error(exc)
    return Response(
        status_code=getattr(exc, "status_code", 400),
        content={
            "success": False,
            "message": getattr(exc, "detail", ""),
            "details": "",
        },
    )


def custom_generic_exception(request: Request, exc: Exception) -> Response:
    """
    Handles generic exceptions and returns a standardized response.

    Args:
        exc (Exception): The exception instance.
        request (Optional[Request]): The HTTP request object (default is None).

    Returns:
        Response: A standardized HTTP response with a generic error message.
    """
    logger.error(exc)
    return Response(
        status_code=500,
        content={
            "success": False,
            "message": "Something went wrong. Try again later.",
            "details": exc.args[0],
        },
    )


def custom_validation_exception(
    request: Request, exc: RequestValidationError
) -> Response:
    """
    Handles validation exceptions and returns a standardized response.

    Args:
        exc (RequestValidationError): The exception instance, expected to have a `errors()` method.
        request (Optional[Request]): The HTTP request object (default is None).

    Returns:
        Response: A standardized HTTP response with validation error details.
    """
    logger.error(exc)
    validation_errors = None
    if hasattr(exc, "errors"):
        validation_errors = exc.errors()[0]
    return Response(
        status_code=422,
        content={
            "success": False,
            "message": f"{validation_errors['loc'][1]} {validation_errors['msg'].lower()}",
            "details": "Request body validation failed",
        },
    )
