import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app.models import Documents


@pytest.mark.asyncio
async def test_create_session_wrong_payload_name(app_client: AsyncClient, session_payload: dict):
    """
    Test the POST /v1/session endpoint with incorrect payload.
    """
    del session_payload["name"]
    response = await app_client.post("/v1/session/", json=session_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["message"] == "name field required"
    

@pytest.mark.asyncio
async def test_create_session_wrong_payload_document(app_client: AsyncClient, session_payload: dict):
    """
    Test the POST /v1/session endpoint with incorrect payload.
    """
    del session_payload["document_id"]
    response = await app_client.post("/v1/session/", json=session_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["message"] == "document_id field required"
    
    
@pytest.mark.asyncio
async def test_create_session_payload(app_client: AsyncClient, session_payload: dict):
    """
    Test the POST /v1/session endpoint with correct payload. But document_id not found.
    """
    response = await app_client.post("/v1/session/", json=session_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Document with ID 100 not found"


@pytest.mark.asyncio
async def test_create_session_payload(
    app_client: AsyncClient, db_session: AsyncSession, session_payload: dict, sample_document: dict
):
    """
    Test the POST /v1/session endpoint with correct payload.
    """
    document_obj = Documents(**sample_document)
    db_session.add(document_obj)
    await db_session.commit()
    await db_session.refresh(document_obj)
    session_payload.update({"document_id": document_obj.id})
    response = await app_client.post("/v1/session/", json=session_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["details"]["session_id"] == 1
    assert response.json()["message"] == "Session created successfully."
    setattr(document_obj, "is_deleted", True)
    db_session.add(document_obj)
    await db_session.commit()
    await db_session.refresh(document_obj)
    

@pytest.mark.asyncio
async def test_chat_wrong_payload(
    app_client: AsyncClient, chat_payload: dict
):
    """
    Test the POST /v1/session/{session_id} endpoint with wrong payload.
    """
    del chat_payload["question"]
    response = await app_client.post("/v1/session/1", json=chat_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["message"] == "question field required"


@pytest.mark.asyncio
async def test_chat_no_session(
    app_client: AsyncClient, chat_payload: dict
):
    """
    Test the POST /v1/session/{session_id} endpoint with no session_id.
    """
    response = await app_client.post("/v1/session/", json=chat_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["message"] == "name field required"
    

@pytest.mark.asyncio
async def test_chat_session_invalid(
    app_client: AsyncClient, chat_payload: dict
):
    """
    Test the POST /v1/session/{session_id} endpoint with no session_id.
    """
    response = await app_client.post("/v1/session/100", json=chat_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Session not found."


@pytest.mark.asyncio
async def test_chat_successful(
    app_client: AsyncClient, chat_payload: dict, sample_pdf, session_payload: dict):
    """
    Test the POST /v1/session/{session_id} endpoint with no session_id.
    Ingest a new file, create a session and chat using that session.
    """
    files = {"new_file": ("wikipedia-4.pdf", sample_pdf, "application/pdf")}
    response = await app_client.post("/v1/document/ingest", files=files)
    assert response.status_code == status.HTTP_200_OK
    ingest_data = response.json()["details"]

    session_payload.update({"document_id": ingest_data["id"]})
    response = await app_client.post("/v1/session/", json=session_payload)
    assert response.status_code == status.HTTP_200_OK
    session_data = response.json()["details"]

    response = await app_client.post(f"/v1/session/{session_data["session_id"]}", json=chat_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Question answered successfully."
