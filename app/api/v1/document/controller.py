"""
This module defines the controller for document management functionality.
It handles the business logic for retrieving, ingesting, and processing documents.
"""

import hashlib
from io import BytesIO
from typing import Any, Dict, List

from crud import DocumentChunkCrud, DocumentCrud
from fastapi import UploadFile
from PyPDF2 import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession
from utils import logger


class DocumentController:
    """
    Controller for managing document-related operations.
    Provides methods to retrieve documents, ingest new documents, and process document chunks.
    """

    def __init__(self):
        """
        Initializes the DocumentController with required CRUD dependencies.
        """
        self.document_crud = DocumentCrud()
        self.document_chunk_crud = DocumentChunkCrud()

    async def get_all_documents(
        self, *, session: AsyncSession, skip: int = 0, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve multiple documents with pagination.

        Args:
            session (AsyncSession): The database session.
            skip (int): The number of records to skip (default: 0).
            limit (int): The maximum number of records to retrieve (default: 10).

        Returns:
            List[Dict[str, Any]]: A list of document objects with metadata.
        """
        logger.info("Inside document controller, executing get_all_documents ...")
        documents = await self.document_crud.get_multi(
            session=session, skip=skip, limit=limit
        )
        result = []
        for document in documents:
            result.append(
                {
                    "id": document.id,
                    "filename": document.filename,
                    "status": document.status,
                    "embedding_model": document.embedding_model,
                    "processing_time": document.processing_time,
                    "metadata_info": document.metadata_info,
                    "is_deleted": document.is_deleted,
                    "created_at": document.created_at,
                    "updated_at": document.updated_at,
                }
            )
        return result

    async def add_document(
        self, *, session: AsyncSession, file: UploadFile
    ) -> Dict[str, Any]:
        """
        Ingest a new document, extract its content, and process it into chunks.

        Args:
            session (AsyncSession): The database session.
            file (UploadFile): The uploaded PDF file to be ingested.

        Returns:
            Dict[str, Any]: Metadata and processing details of the ingested document.
        """
        logger.info("Inside document controller, executing add_document ...")
        file_content = await file.read()
        reader = PdfReader(BytesIO(file_content))
        text_per_page = [page.extract_text() for page in reader.pages]
        new_document_obj = {
            "filename": file.filename,
            "metadata_info": {
                "size": f"{int(len(file_content) / 1024)} KB",
                "pages": len(text_per_page),
                "md5": hashlib.md5(file_content).hexdigest(),
            },
        }
        document_obj = await self.document_crud.create(
            session=session, create_obj=new_document_obj
        )
        last_chunk = await self.document_chunk_crud.process_document_chunks(
            session=session, document_id=document_obj.id, chunks=text_per_page
        )
        processing_time_in_seconds = (
            last_chunk["created_at"] - document_obj.created_at
        ).total_seconds()
        _ = await self.document_crud.update(
            session=session,
            db_obj=document_obj,
            obj_in={
                "processing_time": float(processing_time_in_seconds),
                "status": "COMPLETED",
            },
        )
        return {"id": document_obj.id, "usage": last_chunk["usage"], **new_document_obj}
