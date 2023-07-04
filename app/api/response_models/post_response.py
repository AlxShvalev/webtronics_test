from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.api.response_models.user_response import UserResponse


class PostResponse(BaseModel):
    id: UUID
    title: str
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostWithAuthorResponse(PostResponse):
    author: UserResponse
