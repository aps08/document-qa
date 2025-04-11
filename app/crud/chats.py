from models import Chats
from schemas import ChatCreate

from .base import BaseCrud


class ChatCrud(BaseCrud[Chats, ChatCreate, ChatCreate]):
    def __init__(self):
        super().__init__(model=Chats)