from models import ChatSessions
from schemas import ChatSessionCreate

from .base import BaseCrud


class ChatSessionCrud(BaseCrud[ChatSessions, ChatSessionCreate, ChatSessionCreate]):
    def __init__(self):
        super().__init__(model=ChatSessions)
