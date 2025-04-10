"""
This module defines the `Document` model, which represents a document in the system.
The model includes fields for storing metadata about the document, such as its filename,
status, embedding model, and processing time. It also establishes a relationship with
the `DocumentChunk` model for managing document chunks.

The `Document` model inherits common fields and configurations from the `Base` class.
"""

from typing import Optional, List

from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, id, string


class Documents(Base):
    """
    Represents a document in the system.

    Attributes:
        id (int): The unique identifier for the document.
        filename (str): The name of the file associated with the document.
        status (str): The processing status of the document (default: "PENDING").
        embedding_model (str): The embedding model used for processing the document
            (default: "text-embedding-3-small").
        processing_time (Optional[float]): The time taken to process the document, in seconds.
        chunks (List[DocumentChunk]): The list of chunks associated with the document.
    """

    id: Mapped[id]
    filename: Mapped[string]
    status: Mapped[string] = mapped_column(default="PENDING", nullable=False)
    embedding_model: Mapped[string] = mapped_column(
        default="text-embedding-3-small", nullable=True
    )
    processing_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    chunks: Mapped[List["DocumentChunks"]] = relationship(back_populates="document")
    chat_sessions: Mapped[List["ChatSessions"]] = relationship(
        back_populates="document"
    )
