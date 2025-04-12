"""
This module defines the CRUD operations for managing chat sessions.
It provides functionality to interact with the `ChatSessions` model.
"""

from models import ChatSessions
from schemas import ChatSessionCreate

from .base import BaseCrud


class ChatSessionCrud(BaseCrud[ChatSessions, ChatSessionCreate, ChatSessionCreate]):
    """
    CRUD class for managing chat sessions.
    Inherits common CRUD operations from BaseCrud.
    """
    def __init__(self):
        """
        Initializes the ChatSessionCrud with the ChatSessions model.
        """
        super().__init__(model=ChatSessions)
