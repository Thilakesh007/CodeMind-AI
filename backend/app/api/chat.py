from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any

from app.services.chat_service import chat_with_repository

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

class ChatRequest(BaseModel):
    question: str
    project: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []
    model: Optional[str] = None

@router.post("/")
def chat(request: ChatRequest):
    return StreamingResponse(
        chat_with_repository(
            request.question, request.project, request.history, stream=True, model=request.model
        ),
        media_type="application/x-ndjson"
    )