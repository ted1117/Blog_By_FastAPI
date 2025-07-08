from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schema.comment import CommentRead


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostRead(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class PostReadWithComments(PostRead):
    comments: list["CommentRead"] = []
