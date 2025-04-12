"""
This module defines the CRUD operations for managing chats.
It provides functionality to interact with the `Chats` model.
"""

from models import Chats
from schemas import ChatCreate

from .base import BaseCrud


class ChatCrud(BaseCrud[Chats, ChatCreate, ChatCreate]):
    """
    CRUD class for managing chats.
    Inherits common CRUD operations from BaseCrud.
    """

    def __init__(self):
        """
        Initializes the ChatCrud with the Chats model.
        """
        super().__init__(model=Chats)
