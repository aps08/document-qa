"""
This module defines the CRUD operations for managing documents.
It provides functionality to interact with the `Documents` model.
"""

from models import Documents
from schemas import DocumentCreate, DocumentUpdate

from .base import BaseCrud


class DocumentCrud(BaseCrud[Documents, DocumentUpdate, DocumentCreate]):
    """
    CRUD class for managing documents.
    Inherits common CRUD operations from BaseCrud.
    """
    def __init__(self):
        """
        Initializes the DocumentCrud with the Documents model.
        """
        super().__init__(model=Documents)
