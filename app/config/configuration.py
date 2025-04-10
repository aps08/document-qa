"""
This module defines a configuration class that loads environment variables
into a configuration object. It provides centralized access to application
settings such as the SQLAlchemy database URL and the OpenAI API key.
"""

import os
from typing import cast
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Configuration class that loads environment variables.

    Attributes:
        SQLALCHEMY_DATABASE_URL (str): The database URL for SQLAlchemy/PostgreSQL.
        OPENAI_API_KEY (str): The API key for OpenAI.
    """

    SQLALCHEMY_DATABASE_URL: str = cast(str, os.getenv("SQLALCHEMY_DATABASE_URL"))
    OPENAI_API_KEY: str = cast(str, os.getenv("OPENAI_API_KEY"))
    ENV: str = cast(str, os.getenv("ENV", "development"))

    class Config:
        env_file = ".env"


config = Config()
