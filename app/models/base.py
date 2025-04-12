"""
This base model provides common columns and configurations
for all models. It automatically generates the table name
(__table__) based on the class name.

Examples:
    Class Projects -> "projects" table in the database
    Class UserProjectMapping -> "user_project_mapping" table in the database
"""

import re
from datetime import datetime, timezone
from typing import Annotated, Any

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
string = Annotated[str, mapped_column()]
utc_now = lambda: datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """
    Declarative base class with common table field.
    """

    @declared_attr.directive
    def __tablename__(cls: Any) -> str:
        """Constructs table name using class name"""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    metadata_info: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    def __repr__(self) -> str:
        """
        Returns a string representation of the object, showing all its attributes and their values.
        """
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in vars(self).items()
            if not key.startswith("_")
        )
        return f"<{self.__class__.__name__}({attrs})>"
