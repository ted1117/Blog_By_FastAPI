from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# from app.models.comment import Comment
# from app.models.user import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="posts", cascade="all, delete-orphan")

    # user: Mapped["User"] = relationship(back_populates="posts")
    # comments: Mapped[List["Comment"]] = relationship(
    #     back_populates="posts",
    #     cascade="all, delete-orphan"
    # )
