"""
This module defines Pydantic schemas for various response models used in the application.
These schemas are used for data validation and serialization of API responses.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """
    Schema for metadata information of a document.
    """

    size: str = Field(example="eda4cd10db0fca83dd3f9fddbf1a5c16")
    pages: int = Field(example=5)
    md5: str = Field(example="158 KB")


class DocumentGet(BaseModel):
    """
    Schema for retrieving document details.
    """

    id: int = Field(example=5)
    filename: str = Field(example="paper.pdf")
    status: str = Field(example="COMPLETED")
    embedding_model: str = Field(example="text-embedding-3-small")
    processing_time: float = Field(example=18.672)
    metadata_info: DocumentMetadata
    is_deleted: bool = Field(example=False)
    created_at: datetime
    updated_at: datetime


class DocumentIngestion(BaseModel):
    """
    Schema for document ingestion response.
    """

    id: int = Field(example=5)
    filename: str = Field(example="paper.pdf")
    metadata_info: DocumentMetadata
    usage: int = Field(example=546)


class MetadataInfo(BaseModel):
    """
    Schema for metadata information of a chat.
    """

    chat_completion_id: str = Field(example="chatcmpl-BLMDfmQeqk0N1zdZk9GaeTJQbzs5G")
    usage: int = Field(example=546)


class CreateChatSession(BaseModel):
    """
    Schema for creating a chat session.
    """

    session_id: int = Field(example=5)


class ChatCompletion(BaseModel):
    """
    Schema for chat completion response.
    """

    session_id: int = Field(example=5)
    question: str = Field(example="What is DynamoDB ?")
    answer: str = Field(
        example="Amazon DynamoDB is a database service that stores and retrieves data in key-value pairs."
    )
    metadata_info: MetadataInfo
    chat_id: int = Field(example=5)
    created_at: datetime
