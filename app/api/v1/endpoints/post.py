from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, DbSession, PostId
from app.api.v1.endpoints.comment import router as comment_router
from app.crud.post import create_post, delete_post, get_post, get_posts, update_post
from app.models.post import Post
from app.schema.post import PostCreate, PostRead, PostUpdate

router = APIRouter()


@router.get("/", response_model=list[PostRead], summary="게시글 목록 조회")
def read_posts(
    db: DbSession,
    skip: Annotated[int, Query(ge=0, description="건너뛸 게시글의 수")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="한 번에 가져올 최대 게시글의 수")
    ] = 10,
):
    """게시글을 페이지네이션하여 반환합니다."""
    return get_posts(db, skip, limit)


@router.get("/{post_id}", response_model=PostRead, summary="특정 게시글 조회")
def read_post(post_id: PostId, db: DbSession) -> Post:
    """게시글 ID로 특정 게시글을 조회합니다."""
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_post


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 게시글 생성",
)
def create_new_post(
    user: CurrentUser,
    db: DbSession,
    post_in: PostCreate,
) -> Post:
    """새로운 게시글을 등록합니다."""
    return create_post(db, user.id, post_in)


@router.put("/{post_id}", response_model=PostRead, summary="기존 게시글 수정")
def update_existing_post(
    user: CurrentUser,
    db: DbSession,
    post_id: PostId,
    post_in: PostUpdate,
) -> Post:
    """
    기존 게시글을 수정합니다.

    게시글은 작성자나 관리자만 수정할 수 있으며, 권한이 없는 경우 `403 Fobidden` 오류를 반환합니다.
    """
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.user_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions"
        )

    return update_post(db=db, db_post=db_post, post_in=post_in)


@router.delete("/{post_id}", summary="기존 게시글 삭제")
def delete_existing_post(
    user: CurrentUser,
    db: DbSession,
    post_id: PostId,
):
    """
    기존 게시글을 삭제합니다.

    게시글은 작성자나 관리자만 삭제할 수 있으며, 권한이 없는 경우 `403 Forbidden` 에러를 반환합니다.
    """
    db_post = get_post(db, post_id)

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    if db_post.user_id != user.id or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    delete_post(db, db_post)

    return {"detail": "Post deleted."}


# comment router
router.include_router(comment_router, prefix="/{post_id}/comments", tags=["comments"])
