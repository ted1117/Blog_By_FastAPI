from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Comment
from app.schema.comment import CommentCreate, CommentUpdate


def create_comment(
    db: Session, user_id: int, post_id: int, comment_in: CommentCreate
) -> Comment:
    """새로운 댓글을 DB에 저장합니다."""
    db_comment = Comment(content=comment_in.content, user_id=user_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def get_comment(db: Session, comment_id: int) -> Comment | None:
    """ID로 특정 댓글 한 개를 조회합니다."""
    stmt = select(Comment).where(Comment.id == comment_id)
    return db.execute(stmt).scalar_one_or_none()


def get_comments_by_post(
    db: Session, post_id: int, skip: int = 0, limit: int = 10
) -> Sequence[Comment]:
    """특정 게시글에 작성된 모든 댓글을 페이지네이션하여 조회합니다."""
    stmt = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .order_by(Comment.id.asc())
    )

    return db.execute(stmt).scalars().all()


def get_comments_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> Sequence[Comment]:
    """특정 사용자가 작성한 모든 댓글을 페이지네이션하여 조회합니다."""
    stmt = (
        select(Comment)
        .where(Comment.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Comment.id.asc())
    )

    return db.execute(stmt).scalars().all()


def update_comment(
    db: Session, db_comment: Comment, comment_in: CommentUpdate
) -> Comment:
    """특정 댓글 내용을 수정하여 데이터베이스에 갱신합니다."""
    if comment_in.content is not None:
        db_comment.content = comment_in.content

    db.commit()
    db.refresh(db_comment)

    return db_comment


def delete_comment(db: Session, db_comment: Comment):
    """특정 댓글을 삭제합니다."""
    db.delete(db_comment)
    db.commit()
