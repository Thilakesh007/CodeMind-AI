from fastapi import APIRouter
from pathlib import Path

from app.repository.tree_generator import build_tree

router = APIRouter()


@router.get("/tree/{project_name}")
def get_tree(project_name: str):

    project_path = Path("../repositories") / project_name

    if not project_path.exists():
        return {
            "success": False,
            "message": "Repository not found."
        }

    return {
        "success": True,
        "tree": build_tree(project_path)
    }