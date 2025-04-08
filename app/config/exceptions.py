"""
This module contains custom exception handlers for the FastAPI application.
Each function is designed to handle specific types of exceptions and return
a standardized response format.
"""

from typing import Optional

from config.response import Response
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError


def custom_http_exception(
    exc: HTTPException, request: Optional[Request] = None
) -> Response:
    """
    Handles HTTP exceptions and returns a standardized response.

    Args:
        exc (HTTPException): The exception instance.
        request (Optional[Request]): The HTTP request object (default is None).

    Returns:
        Response: A standardized HTTP response with the exception details.
    """
    status_code = 400
    if hasattr(exc, "status_code"):
        status_code = exc.status_code
    return Response(
        status_code=status_code,
        content={"success": False, "message": exc.detail, "details": None},
    )


def custom_generic_exception(
    exc: Exception, request: Optional[Request] = None
) -> Response:
    """
    Handles generic exceptions and returns a standardized response.

    Args:
        exc (Exception): The exception instance.
        request (Optional[Request]): The HTTP request object (default is None).

    Returns:
        Response: A standardized HTTP response with a generic error message.
    """
    return Response(
        status_code=500,
        content={
            "success": False,
            "message": "Something went wrong. Try again later.",
            "details": exc.args,
        },
    )


def custom_validation_exception(
    exc: RequestValidationError, request: Optional[Request] = None
) -> Response:
    """
    Handles validation exceptions and returns a standardized response.

    Args:
        exc (RequestValidationError): The exception instance, expected to have a `errors()` method.
        request (Optional[Request]): The HTTP request object (default is None).

    Returns:
        Response: A standardized HTTP response with validation error details.
    """
    validation_errors = None
    if hasattr(exc, "errors"):
        validation_errors = exc.errors()[0]
    return Response(
        status_code=422,
        content={
            "success": False,
            "message": "Request body validation failed",
            "details": validation_errors["msg"],
        },
    )
