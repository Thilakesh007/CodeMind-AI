from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any

from app.services.documentation_service import generate_documentation

router = APIRouter(
    prefix="/documentation",
    tags=["Documentation"]
)

class DocumentationQuery(BaseModel):
    question: str
    project: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []
    model: Optional[str] = None

@router.post("/")
def documentation(request: DocumentationQuery):
    return StreamingResponse(
        generate_documentation(
            request.question, request.project, request.history, stream=True, model=request.model
        ),
        media_type="application/x-ndjson"
    )
