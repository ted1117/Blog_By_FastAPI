from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def read_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.post("/users")
def create_user(name: str):
    return {"id": 3, "name": name}

