"""
This module defines Pydantic schemas for various response models used in the application.
These schemas are used for data validation and serialization of API responses.
"""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class DocumentGet(BaseModel):
    """
    Schema for retrieving document details.
    """

    id: int
    filename: str
    status: str
    embedding_model: str
    processing_time: float
    metadata_info: Optional[dict[str, Any]] = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentMetadata(BaseModel):
    """
    Schema for metadata information of a document.
    """

    size: str
    pages: int
    md5: str


class DocumentIngestion(BaseModel):
    """
    Schema for document ingestion response.
    """

    id: int
    filename: str
    metadata_info: DocumentMetadata
    usage: int


class MetadataInfo(BaseModel):
    """
    Schema for metadata information of a chat.
    """

    chat_completion_id: str


class CreateChatSession(BaseModel):
    """
    Schema for creating a chat session.
    """

    session_id: int


class ChatCompletion(BaseModel):
    """
    Schema for chat completion response.
    """

    session_id: int
    question: str
    answer: str
    metadata_info: MetadataInfo
    usage: str
    chat_id: int
    created_at: str
