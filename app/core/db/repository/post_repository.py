from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.db.models import Post
from app.core.db.repository.abstract_repository import AbstractRepository


class PostRepository(AbstractRepository):
    """Repository for Post model."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session, Post)
