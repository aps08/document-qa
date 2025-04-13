"""
This module defines the controller for session management functionality.
It handles the business logic for creating sessions and processing questions.
"""

from typing import Any, Dict

from crud import (
    ChatCrud,
    ChatSessionCrud,
    ChatSessions,
    DocumentChunkCrud,
    DocumentCrud,
    Documents,
)
from fastapi import HTTPException
from schemas import ChatSessionCreate, QuestionRequest
from sqlalchemy.ext.asyncio import AsyncSession
from utils import chat_completion, get_vector, logger


class ChatController:
    """
    Controller for managing QA sessions and questions.
    Provides methods to create chat sessions and process user questions.
    """

    def __init__(self):
        """
        Initializes the ChatController with required CRUD dependencies.
        """
        self.document_crud = DocumentCrud()
        self.chat_session_crud = ChatSessionCrud()
        self.chat_crud = ChatCrud()
        self.document_chunk_crud = DocumentChunkCrud()

    async def create_chat_session(
        self, *, session: AsyncSession, chat_session_data: ChatSessionCreate
    ) -> Dict[str, int]:
        """
        Create a new session with the specified documents.

        Args:
            session (AsyncSession): The database session.
            chat_session_data (ChatSessionCreate): The session data including name, system_message, and document_ids.

        Returns:
            Dict[str, int]: The created session information with the session ID.
        """
        logger.info("Inside chat controller, executing create_chat_session ...")
        document = await self.document_crud.get(
            session=session, field=Documents.id, value=chat_session_data.document_id
        )
        if not document:
            raise HTTPException(
                status_code=404, detail=f"Document with ID {chat_session_data.document_id} not found"
            )
        chat_session_obj = chat_session_data.model_dump()
        chat_session = await self.chat_session_crud.create(
            session=session, create_obj=chat_session_obj
        )
        return {"session_id": chat_session.id}

    async def ask_question(
        self,
        *,
        session: AsyncSession,
        question_info: QuestionRequest,
        chat_session_id: int,
    ) -> Dict[str, Any]:
        """
        Process a user question by performing a similarity search and generating a response.

        Args:
            session (AsyncSession): The database session.
            question_info (QuestionRequest): The question details including text, model, and max tokens.
            chat_session_id (int): The ID of the chat session.

        Returns:
            Dict[str, Any]: The generated response along with metadata and chat details.
        """
        logger.info("Inside chat controller, executing ask_question ...")
        chat_session = await self.chat_session_crud.get(
            session=session, field=ChatSessions.id, value=chat_session_id
        )
        if not chat_session:
            raise HTTPException(status_code=404, detail="Session not found.")
        vector, usage = await get_vector(text=question_info.question)
        similarities_top_three = await self.document_chunk_crud.similarity_search(
            session=session,
            search_query_vector=vector,
            document_id=chat_session.document_id,
        )
        context = "\n\n".join(
            [
                f"{chunk.content} page_number {chunk.page_number}"
                for chunk in similarities_top_three
            ]
        )
        answer, chat_id, answer_usage = await chat_completion(
            context=context,
            system_message=chat_session.system_message,
            question=question_info.question,
            max_tokens=question_info.max_tokens,
            model=question_info.model,
        )
        new_chat_obj = {
            "session_id": chat_session_id,
            "question": question_info.question,
            "answer": answer,
            "metadata_info": {
                "chat_completion_id": chat_id,
                "usage": answer_usage + usage,
                "model": question_info.model,
            },
        }
        chat_obj = await self.chat_crud.create(session=session, create_obj=new_chat_obj)
        return {
            **new_chat_obj,
            "chat_id": chat_obj.id,
            "created_at": chat_obj.created_at,
        }
