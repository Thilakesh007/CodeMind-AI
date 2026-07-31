from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any
from app.services.readme_service import generate_readme

router = APIRouter()

class ReadmeQuery(BaseModel):
    question: str
    project: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []

@router.post("/readme")
def run_readme_query(query: ReadmeQuery):
    return StreamingResponse(
        generate_readme(
            query.question, query.project, query.history, stream=True
        ),
        media_type="application/x-ndjson"
    )
