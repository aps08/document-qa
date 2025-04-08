from api.v1.document.router import document_router
from api.v1.ingestion.router import ingestion_router
from api.v1.qa.router import qa_router
from fastapi import APIRouter

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(ingestion_router, tags=["Document Ingestion"])
api_v1_router.include_router(qa_router, tags=["Document QA"])
api_v1_router.include_router(document_router, tags=["Document Selections"])
