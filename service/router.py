from fastapi import APIRouter, HTTPException
from .schema import TeachersRequest

quote_router = APIRouter()

@quote_router.post("/quote")
def generate_quote(request: TeachersRequest):
    try:
        return {
            "request": request.topics,
            "quote": {
                "total_items": sum(request.topics.values()),
                "topics": request.topics,
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

