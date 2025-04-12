"""
This module defines the API routes for session management functionality.
It includes endpoints for creating new sessions and asking questions within existing sessions.
"""

from api.v1.chats.controller import ChatController
from config import Response
from fastapi import APIRouter, Depends, HTTPException
from schemas import (
    QuestionRequest,
    ChatSessionCreate,
    ChatCompletion,
    CreateChatSession,
)
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_db_session

chats_router = APIRouter(prefix="/session")


@chats_router.post("/", response_model=CreateChatSession)
async def create_session(
    chat_session_data: ChatSessionCreate,
    db_session: AsyncSession = Depends(get_db_session),
):
    """
    Create a new QA session with specified documents.

    Args:
        session_data (SessionCreate): The session data including name, system_message, and document_ids.
        db_session (AsyncSession): The database session.

    Returns:
        dict: A success message with the created session details.
    """
    response = await ChatController().create_chat_session(
        session=db_session, chat_session_data=chat_session_data
    )
    return Response.success(message="Session created successfully.", body=response)


@chats_router.post("/{session_id}", response_model=ChatCompletion)
async def ask_question(
    session_id: int,
    question_data: QuestionRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Ask a question within an existing session.

    Args:
        session_id (int): The ID of the session to ask the question in.
        question_data (QuestionRequest): The question data including the question text, max_tokens and model.
        session (AsyncSession): The database session.

    Returns:
        dict: A success message with the answer to the question.
    """
    if not session_id:
        raise HTTPException(status_code=404, detail="Session not found.")
    response = await ChatController().ask_question(
        session=session, question_info=question_data, chat_session_id=session_id
    )
    return Response.success(message="Question answered successfully.", body=response)
