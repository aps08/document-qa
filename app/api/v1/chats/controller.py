"""
This module defines the controller for session management functionality.
It handles the business logic for creating sessions and processing questions.
"""

from typing import Any, Dict

from crud import ChatSessionCrud, ChatSessions, DocumentCrud, Documents
from fastapi import HTTPException
from schemas import SessionCreate
from sqlalchemy.ext.asyncio import AsyncSession


class ChatController:
    """
    Controller for managing QA sessions and questions.
    """

    def __init__(self):
        self.document_crud = DocumentCrud()
        self.chat_session_crud = ChatSessionCrud()

    async def create_chat_session(
        self, *, session: AsyncSession, chat_session_data: SessionCreate
    ) -> Dict[str, int]:
        """
        Create a new session with the specified documents.

        Args:
            session (AsyncSession): The database session.
            session_data (SessionCreate): The session data including name, system_message, and document_ids.

        Returns:
            Dict[str, Any]: The created session information.
        """
        document = await self.document_crud.get(
            session=session, field=Documents.id, value=chat_session_data.document_id
        )
        if not document:
            raise HTTPException(f"Document with ID {document.id} not found")
        chat_session_obj = chat_session_data.model_dump()
        chat_session = await self.chat_session_crud.create(
            session=session, create_obj=chat_session_obj
        )
        return {"session_id": chat_session.id}
