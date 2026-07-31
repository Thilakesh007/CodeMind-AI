from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any
from app.services.tests_service import generate_tests

router = APIRouter()

class TestQuery(BaseModel):
    question: str
    project: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = []

@router.post("/tests")
def run_tests_query(query: TestQuery):
    return StreamingResponse(
        generate_tests(
            query.question, query.project, query.history, stream=True
        ),
        media_type="application/x-ndjson"
    )
