from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class DocumentGet(BaseModel):
    id: int
    filename: str
    status: str
    embedding_model: str
    processing_time: float
    metadata_info: Optional[dict[str, Any]] = None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
