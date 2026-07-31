from fastapi import APIRouter, HTTPException
import os
import shutil
from app.config_manager import load_config, save_config, AppConfig
from app.vectorstore.chroma_client import client as chroma_client

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/")
def get_settings():
    config = load_config()
    return config.dict()

@router.post("/")
def update_settings(config: AppConfig):
    success = save_config(config)
    if success:
        return {"success": True, "message": "Settings saved successfully"}
    raise HTTPException(status_code=500, detail="Failed to save settings")

@router.post("/clear-db")
def clear_database():
    try:
        # Delete ChromaDB collection
        try:
            chroma_client.delete_collection("codebase")
            # Recreate an empty collection
            chroma_client.get_or_create_collection("codebase")
        except Exception as e:
            print(f"Error resetting chroma collection: {e}")
        
        # Delete repositories folder
        EXTRACT_DIR = "../repositories"
        if os.path.exists(EXTRACT_DIR):
            import stat
            def remove_readonly(func, path, excinfo):
                os.chmod(path, stat.S_IWRITE)
                func(path)
                
            shutil.rmtree(EXTRACT_DIR, onerror=remove_readonly)
            os.makedirs(EXTRACT_DIR, exist_ok=True)
            
        return {"success": True, "message": "Database and repositories cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
