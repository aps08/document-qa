import pytest
from fastapi import status
from app.models import Documents


@pytest.mark.asyncio
def test_get_documents_empty(app_client):
    """
    Test the GET /v1/document/ endpoint when no documents exist.
    """
    response = app_client.get("/v1/document/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] == True
    assert response.json()["details"] == {}


@pytest.mark.asyncio
async def test_get_documents_with_data(app_client, db_session):
    """
    Test the GET /v1/document/ endpoint when documents exist.
    """
    sample_document = {
        "filename": "sample.pdf",
        "status": "COMPLETED",
        "embedding_model": "text-embedding-3-small",
        "processing_time": 12.34,
        "metadata_info": {"size": "150 KB", "pages": 10, "md5": "abc123"},
        "is_deleted": False,
    }
    document_obj = Documents(**sample_document)
    db_session.add(document_obj)
    await db_session.commit()
    await db_session.refresh(document_obj)
    print(document_obj)
    response = app_client.get("/v1/document/")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    assert len(response.json()["details"]) == 1
    assert response.json()["details"][0]["id"] == document_obj.id
    assert response.json()["details"][0]["filename"] == "sample.pdf"
    assert response.json()["details"][0]["status"] == "COMPLETED"
    assert response.json()["details"][0]["metadata_info"]["size"] == "150 KB"
    assert response.json()["details"][0]["metadata_info"]["pages"] == 10