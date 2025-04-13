"""
This module contains test cases for the `/v1/document/` API endpoints.
It includes tests for scenarios where no documents exist and when documents are present in the database.
"""

import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app.models import Documents


@pytest.mark.asyncio
async def test_get_document(app_client: AsyncClient):
    """
    Test the GET /v1/document/ endpoint when no documents exist.
    """
    response = await app_client.get("/v1/document/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert response.json()["message"] == "Retrieved documents informaiton successfully."
    assert response.json()["details"] == {}


@pytest.mark.asyncio
async def test_get_documents(
    app_client: AsyncClient, db_session: AsyncSession, sample_document: dict
):
    """
    Test the GET /v1/document/ endpoint when documents exist.
    """
    document_obj = Documents(**sample_document)
    db_session.add(document_obj)
    await db_session.commit()
    await db_session.refresh(document_obj)

    response = await app_client.get("/v1/document/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Retrieved documents informaiton successfully."
    documents = response.json()["details"]
    for document in documents:
        if document["id"] == document_obj.id:
            current_document = document
            break
    assert current_document["status"] == "COMPLETED"
    assert current_document["metadata_info"]["size"] == "150 KB"
    assert current_document["metadata_info"]["pages"] == 10
    assert current_document["metadata_info"]["md5"] == "abc123"
    setattr(document_obj, "is_deleted", True)
    db_session.add(document_obj)
    await db_session.commit()

@pytest.mark.asyncio
async def test_ingest_document(app_client: AsyncClient, sample_pdf):
    """
    Test the POST /v1/document/ingest endpoint to upload a PDF document.
    """
    files = {"new_file": ("wikipedia-4.pdf", sample_pdf, "application/pdf")}
    response = await app_client.post("/v1/document/ingest", files=files)
    assert response.status_code == status.HTTP_200_OK
    assert "size" in response.json()["details"]["metadata_info"]
    assert "pages" in response.json()["details"]["metadata_info"]
    assert "md5" in response.json()["details"]["metadata_info"]
    assert response.json()["details"]["filename"] == "wikipedia-4.pdf"
    assert response.json()["message"] == "Document ingested successfully."
    

@pytest.mark.asyncio
async def test_ingest_document_not_pdf(app_client: AsyncClient, sample_pdf):
    """
    Test the POST /v1/document/ingest endpoint to upload a another document.
    """
    files = {"new_file": ("wikipedia-4.pdf", sample_pdf, "application/json")}
    response = await app_client.post("/v1/document/ingest", files=files)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["message"] == "Only PDF file is accepted."
