from fastapi import APIRouter

router = APIRouter()

@router.get("/items")
def get_items():
    return [{"id": 1, "title": "asdf", "content": "qwerty"}]

@router.get("/items")
def get_item():
    return {"id": 1, "title": "asdf", "content": "qwerty"}

@router.post("/items")
def post_items():
    return {"id": 2, "title": "new article", "content": "New Content!"}