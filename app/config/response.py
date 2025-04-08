"""
This module defines a custom `Response` class that extends FastAPI's `JSONResponse`.
It provides utility methods for creating standardized HTTP responses.
"""

from typing import Optional, TypeAlias, Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

JSONContent: TypeAlias = Union[dict, list]


class Response(JSONResponse):
    """
    A custom response class that extends FastAPI's `JSONResponse` to provide
    additional functionality for creating standardized responses.
    """

    def __init__(self, content: JSONContent, status_code: int) -> None:
        """
        Initializes the custom Response object.

        Args:
            content (JSONContent): The content of the response, which must be a JSON object (dictionary or list).
            status_code (int): The HTTP status code for the response.
        """
        super().__init__(content, status_code)

    def json(self) -> bytes:
        """
        Returns the raw JSON body of the response.

        Returns:
            bytes: The raw JSON body of the response.
        """
        return self.body

    @staticmethod
    def success(
        *, message: str, status_code: int = 200, body: Optional[JSONContent] = None
    ) -> "Response":
        """
        Creates a standardized success response.

        Args:
            message (str): A message describing the success.
            status_code (int, optional): The HTTP status code for the response. Defaults to 200.
            body (Optional[JSONContent], optional): Additional data to include in the response body. Defaults to None.

        Returns:
            Response: A custom Response object with the success details.
        """
        return Response(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "details": jsonable_encoder(body) if body else {},
            },
        )
