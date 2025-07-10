from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schema.post import PostCreate, PostUpdate


def create_post(db: Session, user_id: int, post_in: PostCreate) -> Post:
    """게시글을 생성합니다."""
    db_post = Post(title=post_in.title, content=post_in.content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int) -> Post | None:
    """게시글 하나를 조회합니다."""
    stmt = select(Post).where(Post.id == post_id)
    return db.execute(stmt).scalar_one_or_none()


def get_posts(db: Session, skip: int = 0, limit: int = 10) -> Sequence[Post]:
    """게시글 목록을 조회합니다."""
    stmt = select(Post).offset(skip).limit(limit).order_by(Post.id.desc())
    return db.execute(stmt).scalars().all()


def update_post(db: Session, db_post: Post, post_in: PostUpdate) -> Post:
    """기존 게시글을 수정합니다."""
    if post_in.title is not None:
        db_post.title = post_in.title
    if post_in.content is not None:
        db_post.content = post_in.content

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, db_post: Post):
    """기존 게시글을 삭제합니다."""
    db.delete(db_post)
    db.commit()
