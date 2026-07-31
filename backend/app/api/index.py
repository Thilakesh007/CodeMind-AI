from fastapi import APIRouter

from app.services.index_service import index_repository


router = APIRouter()


@router.post("/index")
def index_project(
    project_name: str
):

    return index_repository(
        project_name
    )