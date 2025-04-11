from models import Documents
from schemas import DocumentCreate, DocumentUpdate

from .base import BaseCrud


class DocumentCrud(BaseCrud[Documents, DocumentUpdate, DocumentCreate]):
    def __init__(self):
        super().__init__(model=Documents)
