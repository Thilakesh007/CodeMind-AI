from fastapi import APIRouter, HTTPException
import os
import shutil
from datetime import datetime
from app.vectorstore.chroma_client import delete_project_vectors

router = APIRouter()

EXTRACT_DIR = "../repositories"

@router.get("/projects")
def list_projects():
    projects = []
    
    if os.path.exists(EXTRACT_DIR):
        for item in os.listdir(EXTRACT_DIR):
            item_path = os.path.join(EXTRACT_DIR, item)
            if os.path.isdir(item_path):
                # Basic info about the project
                stat = os.stat(item_path)
                projects.append({
                    "name": item,
                    "indexed_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "path": item_path
                })
                
    return {"success": True, "projects": projects}

@router.delete("/projects/{project_name}")
def delete_project(project_name: str):
    project_path = os.path.join(EXTRACT_DIR, project_name)
    
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
        
    try:
        # 1. Delete physical files (handle read-only files on Windows)
        import stat
        def remove_readonly(func, path, excinfo):
            os.chmod(path, stat.S_IWRITE)
            func(path)
            
        shutil.rmtree(project_path, onerror=remove_readonly)
        
        # 2. Delete vectors from ChromaDB
        delete_project_vectors(project_name)
        
        return {"success": True, "message": f"Project {project_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")
