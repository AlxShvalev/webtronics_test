from datetime import datetime

from pydantic import BaseModel

# from app.api.response_models.user_response import UserResponse


class PostResponse(BaseModel):
    title: str
    text: str
    # author: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
