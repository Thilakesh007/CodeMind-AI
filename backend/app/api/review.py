from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any

from app.services.review_service import review_codebase

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)

class ReviewRequest(BaseModel):
    question: str
    project: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []

@router.post("/")
def review(request: ReviewRequest):
    return StreamingResponse(
        review_codebase(
            request.question, request.project, request.history, stream=True
        ),
        media_type="application/x-ndjson"
    )
