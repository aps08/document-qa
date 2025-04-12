import hashlib
from io import BytesIO
from typing import Any, Dict, List
from fastapi import UploadFile
from utils import get_vector
from crud import DocumentCrud, DocumentChunkCrud
from sqlalchemy.ext.asyncio import AsyncSession
from PyPDF2 import PdfReader


class DocumentController:

    def __init__(self):
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
            List of document objects.
        """
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
