from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    """Тело ответа для модели User."""

    id: UUID
    username: str
    name: str
    surname: str | None
    email: str

    class Config:
        orm_mode = True


class UserLoginResponse(BaseModel):
    """Тело ответа при аутентификации."""

    access_token: str
    refresh_token: str
