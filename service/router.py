from fastapi import APIRouter

quote_router = APIRouter()

@quote_router.get("/")
def read_root():
    return {"message": "Hello World"}
