from pydantic import Field

from app.api.request_models.request_base import RequestBaseModel


class PostCreateRequest(RequestBaseModel):
    title: str = Field(..., min_length=2, max_length=500)
    text: str


class PostUpdateRequest(RequestBaseModel):
    title: str | None
    text: str | None
