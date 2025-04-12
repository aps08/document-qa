"""
This module defines the CRUD operations for managing document chunks.
It provides functionality to process and store document chunks, as well as perform similarity searches.
"""

from typing import List, Dict, Any

from sqlalchemy import select
from models import DocumentChunks
from schemas import ChunkCreate
from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseCrud
from utils import get_vector


class DocumentChunkCrud(BaseCrud[DocumentChunks, ChunkCreate, ChunkCreate]):
    """
    CRUD class for managing document chunks.
    Provides methods to process document chunks and perform similarity searches.
    """
    def __init__(self):
        """
        Initializes the DocumentChunkCrud with the DocumentChunks model.
        """
        super().__init__(model=DocumentChunks)

    async def process_document_chunks(
        self, *, session: AsyncSession, document_id: int, chunks: List[str]
    ) -> Dict[str, Any]:
        """
        Processes and stores document chunks by generating embeddings for each chunk.

        Args:
            session (AsyncSession): The database session.
            document_id (int): The ID of the document to which the chunks belong.
            chunks (List[str]): The list of text chunks to process.

        Returns:
            Dict[str, Any]: A dictionary containing the creation timestamp and total token usage.
        """
        total_usage = 0
        for page_number, content in enumerate(chunks, 1):
            vector, usage = get_vector(text=content)
            new_chunk_obj = {
                "page_number": page_number,
                "content": content,
                "document_id": document_id,
                "embedding": vector,
                "metadata_info": {"usage": usage},
            }
            total_usage += usage
            chunk_obj = await self.create(session=session, create_obj=new_chunk_obj)
        return {"created_at": chunk_obj.created_at, "usage": total_usage}

    async def similarity_search(
        self,
        *,
        session: AsyncSession,
        document_id: int,
        search_query_vector: List[float]
    ) -> List[Any]:
        """
        Performs a similarity search on document chunks using a query vector.

        Args:
            session (AsyncSession): The database session.
            document_id (int): The ID of the document to search within.
            search_query_vector (List[float]): The query vector for similarity search.

        Returns:
            List[Any]: A list of the most similar document chunks.
        """
        return await session.scalars(
            select(DocumentChunks)
            .where(DocumentChunks.document_id == document_id)
            .order_by(DocumentChunks.embedding.cosine_distance(search_query_vector))
            .limit(3)
        )
