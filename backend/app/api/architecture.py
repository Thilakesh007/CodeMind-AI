from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any

from app.services.architecture_service import analyze_architecture

router = APIRouter(
    prefix="/architecture",
    tags=["Architecture"]
)

class ArchitectureRequest(BaseModel):
    question: str
    project: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []

@router.post("/")
def architecture(request: ArchitectureRequest):
    return StreamingResponse(
        analyze_architecture(
            request.question, request.project, request.history, stream=True
        ),
        media_type="application/x-ndjson"
    )
