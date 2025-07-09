from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DbSession
from app.core.security import create_access_token, verify_password
from app.crud.user import create_user, get_user_by_email
from app.schema.token import Token
from app.schema.user import UserCreate

router = APIRouter()

AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/login", response_model=Token, summary="로그인")
def login(db: DbSession, form_data: AuthForm) -> dict[str, str]:
    """
    회원 로그인을 진행하여 액세스 토큰을 반환합니다.

    이메일이나 비밀번호가 틀린 경우, `400 BAD REQUEST` 에러를 반환합니다.
    """
    user = get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED, summary="회원가입")
def signup(user: UserCreate, db: DbSession):
    """
    회원가입을 진행합니다.

    이미 가입된 회원이면 `400 BAD REQUEST`를 반환합니다.
    """
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered."
        )

    create_user(db, user)

    return {"detail": "Signup Success"}
