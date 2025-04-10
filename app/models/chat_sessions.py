"""
This module defines the `ChatSessions` model, which represents chat sessions in the system.
Each chat session is associated with a specific document and contains metadata such as
the session name and an optional system message.

The `ChatSessions` model inherits common fields and configurations from the `Base` class.
"""

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, id, string


class ChatSessions(Base):
    """
    Represents a chat session in the system.

    Attributes:
        id (int): The unique identifier for the chat session.
        name (str): The name of the chat session.
        system_message (Optional[str]): A system message associated with the session.
        document_id (int): The ID of the document associated with this chat session.
        document (Document): The document associated with this chat session.
    """

    id: Mapped[id]
    name: Mapped[string]
    system_message: Mapped[Optional[str]] = mapped_column(nullable=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)

    document: Mapped["Documents"] = relationship(back_populates="chat_sessions")
    chats: Mapped[List["Chats"]] = relationship(back_populates="session")
