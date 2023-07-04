from pydantic import EmailStr, Field, SecretStr, StrictStr

from app.api.request_models.request_base import RequestBaseModel


class UserCreateRequest(RequestBaseModel):
    """Request body for user register."""

    username: StrictStr = Field(min_length=3, max_length=100)
    name: StrictStr = Field(min_length=1, max_length=100)
    surname: StrictStr | None
    email: EmailStr
    password: SecretStr


class LoginRequest(RequestBaseModel):
    """Request body for user authentication."""

    username: StrictStr
    password: SecretStr
