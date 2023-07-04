import abc
from typing import Optional, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions

DatabaseModel = TypeVar("DatabaseModel")


class AbstractRepository(abc.ABC):
    """Abstract class. For pattern Repository realisation."""

    def __init__(self, session: AsyncSession, model: DatabaseModel) -> None:
        self._session = session
        self._model = model

    async def get_or_none(self, instance_id: UUID) -> Optional[DatabaseModel]:
        """Get db object by ID. Else returns None."""
        stmt = select(self._model).where(self._model.id == instance_id)
        db_obj = await self._session.execute(stmt)
        return db_obj.scalars().first()

    async def get(self, instance_id) -> DatabaseModel:
        """Get db object by ID. Else raise exception."""
        db_obj = await self.get_or_none(instance_id)
        if db_obj is None:
            raise exceptions.ObjectNotFoundError(self._model, instance_id)
        return db_obj

    async def create(self, instance: DatabaseModel) -> DatabaseModel:
        """Create new object to database."""
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError:
            raise exceptions.ObjectAlreadyxistsError(instance)
        await self._session.refresh(instance)
        return instance

    async def update(self, instance: DatabaseModel) -> DatabaseModel:
        """Update object in database."""
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def update_all(self, instances: list[DatabaseModel]) -> list[DatabaseModel]:
        """Update multi objects in database."""
        self._session.add_all(instances)
        await self._session.commit()
        return instances

    async def get_all(self) -> list[DatabaseModel]:
        """Get all objects from database."""
        stmt = select(self._model)
        db_objs = await self._session.execute(stmt)
        return db_objs.scalars().all()

    async def delete(self, instance) -> DatabaseModel:
        """Delete object from database."""
        await self._session.delete(instance)
        await self._session.commit()
        return instance
