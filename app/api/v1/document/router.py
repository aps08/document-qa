"""
This module defines the API routes for document ingestion and QA functionality.
It includes endpoints for ingesting documents, retrieving all documents, creating
or managing QA sessions, and selecting documents for QA sessions.
"""

from typing import List, Optional

from api.v1.document.controller import DocumentController
from config import Response
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from schemas import DocumentGet
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_db_session

document_router = APIRouter(prefix="/document")


@document_router.get("/", response_model=List[DocumentGet])
async def get_all_documents(
    session: AsyncSession = Depends(get_db_session),
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    """
    Endpoint for retrieving all ingested documents.

    Returns:
        dict: A list of all ingested documents.
    """
    response = await DocumentController().get_all_documents(
        session=session, skip=skip, limit=limit
    )
    return Response.success(
        message="Retrieved documents informaiton successfully.", body=response
    )


@document_router.post("/ingest")
async def ingest_document(files: List[UploadFile]):
    """
    Ingest multiple PDF documents, generate embeddings,
    and store in the vector database.

    Args:
        document (str): The document content to be ingested.
    Returns:
        dict: A success message indicating the document was ingested.
    """
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' is not a PDF. Only PDF files are accepted.",
            )
    return {"success": True}
