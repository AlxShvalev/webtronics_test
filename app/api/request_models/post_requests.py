from pydantic import Field

from app.api.request_models.request_base import RequestBaseModel


class PostCreateRequest(RequestBaseModel):
    """Request model for Post create body."""

    title: str = Field(..., min_length=2, max_length=500)
    text: str


class PostUpdateRequest(RequestBaseModel):
    """Request model for Post update body."""

    title: str | None
    text: str | None
