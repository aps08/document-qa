from typing import Any, Dict, List

from crud import DocumentCrud
from sqlalchemy.ext.asyncio import AsyncSession


class DocumentController:

    def __init__(self):
        self.document_crud = DocumentCrud()

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
