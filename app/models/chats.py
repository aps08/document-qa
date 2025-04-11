"""
This module defines the `Chats` model, which represents individual chat interactions
within a chat session. Each chat contains a question, an answer, and usage metadata,
and is associated with a specific chat session.

The `Chats` model inherits common fields and configurations from the `Base` class.
"""

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, id, string


class Chats(Base):
    """
    Represents an individual chat interaction within a chat session.

    Attributes:
        id (int): The unique identifier for the chat.
        session_id (int): The ID of the chat session this chat belongs to.
        question (str): The question asked in the chat.
        answer (str): The answer provided in the chat.
        usage (Optional[str]): Metadata about the usage of the chat (e.g., token usage).
        session (ChatSessions): The chat session associated with this chat.
    """

    id: Mapped[id]
    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.id"), nullable=False
    )
    question: Mapped[string]
    answer: Mapped[string]
    usage: Mapped[Optional[string]] = mapped_column(nullable=True)

    session: Mapped["ChatSessions"] = relationship(back_populates="chats")
