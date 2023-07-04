from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    """Body response for User model."""

    id: UUID
    username: str
    name: str
    surname: str | None
    email: str

    class Config:
        orm_mode = True


class UserLoginResponse(BaseModel):
    """Body response for authentication."""

    access_token: str
    refresh_token: str
