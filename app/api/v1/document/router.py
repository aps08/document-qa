"""
This module defines the API routes for document ingestion and QA functionality.
It includes endpoints for ingesting documents, retrieving all documents, creating
or managing QA sessions, and selecting documents for QA sessions.
"""

from fastapi import APIRouter, HTTPException, UploadFile
from typing import Optional, List

document_router = APIRouter(prefix="/document")


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


@document_router.get("/")
async def get_all_documents():
    """
    Endpoint for retrieving all ingested documents.

    Returns:
        dict: A list of all ingested documents.
    """
    return {"success": True}


@document_router.post("/qa/{session_id}")
async def create_session_or_post_question(
    session_id: Optional[int] = None, question: Optional[str] = None
):
    """
    Endpoint for creating a QA session or posting a question to an existing session.

    Args:
        session_id (Optional[int]): The session ID. If not provided, a new session is created.
        question (Optional[str]): The question to be posted in the session.
    Returns:
        dict: A success message with session details or the question response.
    """
    if not session_id is None:
        return {"success": True, "message": "New session created"}
    return {"success": True}


@document_router.put("/select/{session_id}")
async def select_document_in_qa(document_ids: List[int], session_id: int = None):
    """
    Endpoint for selecting one or more documents in the QA section.

    Args:
        session_id (int): The session ID where the documents will be added.
        document_ids (List[int]): A list of document IDs to be added to the session.

    Returns:
        dict: A success message if the documents are added to the session.
    """
    if not session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True, "message": "Document added to session"}
