"""
This module defines the `DocumentChunk` model, which represents chunks of a document.
Each chunk contains a portion of the document's content, its embedding vector, and
the page number it belongs to. The model establishes a relationship with the `Document`
model, allowing chunks to be associated with a specific document.

The `DocumentChunk` model inherits common fields and configurations from the `Base` class.
"""

from typing import Optional, List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .base import Base, id


class DocumentChunks(Base):
    """
    Represents a chunk of a document.

    Attributes:
        id (int): The unique identifier for the document chunk.
        document_id (int): The ID of the document this chunk belongs to.
        content (str): The content of the chunk.
        embedding (Optional[list]): The embedding vector for the chunk's content.
        page_number (Optional[int]): The page number of the document this chunk belongs to.
        document (Document): The document associated with this chunk.
    """

    id: Mapped[id]
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    embedding: Mapped[Optional[List[float]]] = mapped_column(
        Vector(1536), nullable=True
    )
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    document: Mapped["Documents"] = relationship(back_populates="chunks")
