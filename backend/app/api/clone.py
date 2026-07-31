from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import shutil
import git
from pathlib import Path

router = APIRouter()

EXTRACT_DIR = "../repositories"
Path(EXTRACT_DIR).mkdir(exist_ok=True)

class CloneRequest(BaseModel):
    url: str

@router.post("/clone")
def clone_repository(request: CloneRequest):
    try:
        # Extract project name from URL
        repo_name = request.url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
            
        target_path = os.path.join(EXTRACT_DIR, repo_name)
        
        # If it already exists, remove it first
        if os.path.exists(target_path):
            shutil.rmtree(target_path, ignore_errors=True)
            
        # Clone the repository
        git.Repo.clone_from(request.url, target_path)
        
        return {
            "success": True,
            "message": "Repository cloned successfully.",
            "repository": repo_name,
            "location": target_path
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")
