# FastAPI로 구동하는 블로그
## 목차
- [디렉토리 구조](#디렉토리-구조)
- [기능](#기능)
- [엔드포인트](#엔드포인트)

## 디렉토리 구조
```
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── app
│   ├── api
│   │   ├── deps.py
│   │   └── v1
│   │       ├── endpoints
│   │       │   ├── auth.py
│   │       │   ├── comment.py
│   │       │   ├── item.py
│   │       │   ├── post.py
│   │       │   └── user.py
│   │       └── routers.py
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── crud
│   │   ├── comment.py
│   │   ├── post.py
│   │   └── user.py
│   ├── db
│   │   ├── base.py
│   │   └── session.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── comment.py
│   │   ├── post.py
│   │   └── user.py
│   └── schema
│   │   ├── comment.py
│   │   ├── post.py
│   │   ├── token.py
│   │   └── user.py
├── pyproject.toml
├── README.md
├── requirements.txt
└── test.db
```

## 기능
- 회원
  - 회원가입
  - 로그인
- 게시글
  - CRUD
- 댓글
  - CRUD

## 엔드포인트
| Category | Method | Endpoint         | Description           |
| ------ | ------ | ---------------- | --------------------- |
| **게시글** | GET    | /api/v1/posts/      | 게시글 목록 조회      |
| | POST   | /api/v1/posts/      | 게시글 작성           |
| | GET    | /api/v1/posts/{id}/ | 특정 게시글 상세 조회 |
| | PUT    | /api/v1/posts/{id}/ | 게시글 수정           |
| | DELETE | /api/v1/posts/{id}/ | 게시글 삭제           |
| **댓글** | GET    | /api/v1/posts/{post_id}/comments/   | 게시글 內 댓글 목록 조회        |
| | GET | /api/v1/posts/{post_id}/comments/{comment_id}/ | 게시글 內 특정 댓글 상세 조회 |
| | POST   | /api/v1/posts/{post_id}/comments/   | 댓글 작성             |
| | PUT | /api/v1/posts/{post_id}/comments/{comment_id}/ | 댓글 수정 |
| | DELETE | /api/v1/posts/{post_id}/comments/{comment_id}/ | 댓글 삭제 |
| **회원** | POST | /api/v1/users/signup/ | 회원 가입 |
| | POST | /api/v1/users/login/ | 로그인 |
