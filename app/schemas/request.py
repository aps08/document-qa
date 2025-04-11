from typing import List, Optional

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    pass


class DocumentUpdate(BaseModel):
    pass


class SessionCreate(BaseModel):
    name: str
    document_id: int
    system_message: Optional[str] = ""


class QuestionRequest(BaseModel):
    question: str
    max_tokens: Optional[int] = 300
