"""
This module defines Pydantic schemas for request models used in the application.
These schemas are used for data validation and serialization of API requests.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    """
    Schema for creating a new document.
    """

    pass


class DocumentUpdate(BaseModel):
    """
    Schema for updating an existing document.
    """

    pass


class ChatCreate(BaseModel):
    """
    Schema for creating a new chat.
    """

    pass


class ChunkCreate(BaseModel):
    """
    Schema for creating a new document chunk.
    """

    pass


class ChatSessionCreate(BaseModel):
    """
    Schema for creating a new chat session.
    """

    name: str
    document_id: int
    system_message: Optional[str] = ""


class OpenAIModel(str, Enum):
    """
    Enum for supported OpenAI models.
    """

    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0125 = "gpt-3.5-turbo-0125"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"
    GPT_4_0125_PREVIEW = "gpt-4-0125-preview"


class QuestionRequest(BaseModel):
    """
    Schema for submitting a question to the system.
    """

    question: str
    model: Optional[OpenAIModel] = OpenAIModel.GPT_3_5_TURBO
    max_tokens: Optional[int] = 300
