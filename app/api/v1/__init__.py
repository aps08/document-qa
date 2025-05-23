from api.v1.chats.router import chats_router
from api.v1.document.router import document_router
from fastapi import APIRouter

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(document_router, tags=["Document"])
api_v1_router.include_router(chats_router, tags=["Chats"])
