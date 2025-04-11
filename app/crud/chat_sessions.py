from models import ChatSessions
from schemas import SessionCreate

from .base import BaseCrud


class ChatSessionCrud(BaseCrud[ChatSessions, SessionCreate, SessionCreate]):
    def __init__(self):
        super().__init__(model=ChatSessions)
