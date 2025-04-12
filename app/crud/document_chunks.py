"""
This module defines the CRUD operations for managing document chunks.
It provides functionality to process and store document chunks, as well as perform similarity searches.
"""

from typing import Any, Dict, List

from models import DocumentChunks
from schemas import ChunkCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_vector, logger

from .base import BaseCrud


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
        logger.info("Inside documentchunk crud, executing process_document_chunks ...")
        total_usage = 0
        chunk_objs = []
        for page_number, content in enumerate(chunks, 1):
            vector, usage = await get_vector(text=content)
            new_chunk_obj = {
                "page_number": page_number,
                "content": content,
                "document_id": document_id,
                "embedding": vector,
                "metadata_info": {"usage": usage},
            }
            total_usage += usage
            chunk_objs.append(DocumentChunks(**new_chunk_obj))
            if len(chunk_objs) > 10:
                last_obj = chunk_objs[-1]
                session.add_all(chunk_objs)
                await session.commit()
                chunk_objs = []
        if chunk_objs:
            last_obj = chunk_objs[-1]
            session.add_all(chunk_objs)
            await session.commit()
        return {"created_at": last_obj.created_at, "usage": total_usage}

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
        logger.info("Inside documentchunk crud, executing similarity_search ...")
        return await session.scalars(
            select(DocumentChunks)
            .where(DocumentChunks.document_id == document_id)
            .order_by(DocumentChunks.embedding.cosine_distance(search_query_vector))
            .limit(3)
        )
