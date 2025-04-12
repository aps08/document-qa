"""
This module defines a generic `BaseCrud` class that provides common CRUD operations
for any SQLAlchemy model. It includes methods for retrieving, creating, updating,
and deleting records in the database, with support for soft deletion.

The `BaseCrud` class is designed to work with any model that inherits from the `Base`
class and includes an `is_deleted` field for soft deletion.
"""

from typing import Any, Generic, List, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from models import Base
from pydantic import BaseModel
from sqlalchemy import Column, false, select
from sqlalchemy.ext.asyncio import AsyncSession
from utils import logger

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    A generic CRUD class that provides common database operations for any model.

    Attributes:
        model (Type[ModelType]): The SQLAlchemy model class to perform operations on.

    Methods:
        get: Retrieve a single record by a specific field and value.
        get_multi: Retrieve multiple records with optional pagination.
        create: Create a new record in the database.
        update: Update an existing record in the database.
        delete: Soft delete a record by setting `is_deleted` to True.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initializes the BaseCrud instance with the specified model.

        Args:
            model (Type[ModelType]): The SQLAlchemy model class to perform operations on.
        """
        self.model = model

    async def get(
        self, *, session: AsyncSession, field: Column, value: Any
    ) -> ModelType | None:
        """
        Retrieve a single record by a specific field and value, ensuring `is_deleted` is False.

        Args:
            session (AsyncSession): The database session.
            field (Column): The column to filter by.
            value (Any): The value to filter by.

        Returns:
            ModelType | None: The retrieved record, or None if not found.
        """
        logger.info("Inside basecrud, executing get ...")
        query = (
            select(self.model)
            .where(field == value, self.model.is_deleted.is_(false()))
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, *, session: AsyncSession, skip: int = 0, limit: int = 10
    ) -> List[ModelType] | list:
        """
        Retrieve multiple records with optional pagination, ensuring `is_deleted` is False.

        Args:
            session (AsyncSession): The database session.
            skip (int): The number of records to skip (default: 0).
            limit (int): The maximum number of records to retrieve (default: 10).

        Returns:
            List[ModelType] | list: A list of retrieved records.
        """
        logger.info("Inside basecrud, executing get_multi ...")
        query = (
            select(self.model)
            .where(self.model.is_deleted.is_(false()))
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def create(
        self, *, session: AsyncSession, create_obj: CreateSchemaType
    ) -> ModelType:
        """
        Create a new record in the database.

        Args:
            session (AsyncSession): The database session.
            create_obj (CreateSchemaType): The data for the new record.

        Returns:
            ModelType: The created record.
        """
        logger.info("Inside basecrud, executing create ...")
        obj_in_data = jsonable_encoder(create_obj)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, *, session: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update an existing record in the database.

        Args:
            session (AsyncSession): The database session.
            db_obj (ModelType): The existing record to update.
            obj_in (UpdateSchemaType): The updated data.

        Returns:
            ModelType: The updated record.
        """
        logger.info("Inside basecrud, executing update ...")
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, *, session: AsyncSession, db_obj: ModelType) -> ModelType:
        """
        Soft delete a record by setting `is_deleted` to True.

        Args:
            session (AsyncSession): The database session.
            db_obj (ModelType): The record to delete.

        Returns:
            ModelType: The soft-deleted record.
        """
        logger.info("Inside basecrud, executing delete ...")
        db_obj.is_deleted = True
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
