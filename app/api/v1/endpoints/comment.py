from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CommentId, CurrentUser, DbSession, PostId
from app.crud.comment import (
    create_comment,
    delete_comment,
    get_comment,
    get_comments_by_post,
    update_comment,
)
from app.models import Comment
from app.schema.comment import CommentCreate, CommentRead, CommentUpdate

router = APIRouter()


@router.get("/{comment_id}", response_model=CommentRead, summary="특정 댓글 조회")
def read_comment(comment_id: CommentId, db: DbSession) -> Comment:
    """
    댓글 ID를 이용하여 특정 댓글을 조회합니다.
    해당 댓글이 없으면 `404 Not Found`를 반환합니다.
    """
    db_comment = get_comment(db, comment_id)

    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
        )

    return db_comment


@router.get("/", response_model=list[CommentRead], summary="게시글 댓글 목록 조회")
def read_comments(
    post_id: PostId,
    db: DbSession,
    skip: Annotated[int, Query(ge=0, description="건너뛸 댓글 수")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="가져올 최대 댓글 수")] = 10,
):
    """게시글 ID에 해당하는 댓글 목록을 페이지네이션하여 반환합니다."""
    return get_comments_by_post(db, post_id, skip, limit)


@router.post(
    "/",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 댓글 작성",
)
def create_new_comment(
    post_id: PostId,
    user: CurrentUser,
    db: DbSession,
    comment_in: CommentCreate,
) -> Comment:
    """
    특정 게시글에 새로운 댓글을 등록합니다.

    API 호출 시 인증(로그인)이 필요합니다.
    """
    return create_comment(db, user.id, post_id, comment_in)


@router.put("/{comment_id}", response_model=CommentRead, summary="기존 댓글 수정")
def update_existing_comment(
    post_id: PostId,
    comment_id: CommentId,
    user: CurrentUser,
    db: DbSession,
    comment_in: CommentUpdate,
) -> Comment:
    """
    기존 댓글 내용을 수정합니다.

    댓글은 작성자 혹은 관리자만 수정할 수 있으며, 권한이 없는 경우 `403 Forbidden` 에러를 반환합니다.
    """
    db_comment = get_comment(db, comment_id)

    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
        )

    if db_comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Access."
        )

    if db_comment.user_id != user.id or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions."
        )

    return update_comment(db, db_comment, comment_in)


@router.delete(
    "/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="기존 댓글 삭제"
)
def delete_existing_comment(
    post_id: PostId,
    comment_id: CommentId,
    user: CurrentUser,
    db: DbSession,
):
    """
    특정 댓글을 삭제합니다.

    댓글은 작성자와 관리자만 삭제할 수 있으며, 권한이 없으면 `403 Forbidden` 에러를 반환합니다.
    """
    db_comment = get_comment(db, comment_id)

    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
        )

    if db_comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Access."
        )

    if db_comment.user_id != user.id or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions."
        )

    delete_comment(db, db_comment)

    return None
