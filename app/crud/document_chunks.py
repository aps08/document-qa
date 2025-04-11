from models import DocumentChunks
from schemas import ChunkCreate

from .base import BaseCrud


class DocumentChunkCrud(BaseCrud[DocumentChunks, ChunkCreate, ChunkCreate]):
    def __init__(self):
        super().__init__(model=DocumentChunks)