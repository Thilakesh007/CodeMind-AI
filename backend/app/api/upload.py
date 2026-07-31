from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil
import zipfile
import os

router = APIRouter()

UPLOAD_DIR = "../uploads"
EXTRACT_DIR = "../repositories"

Path(UPLOAD_DIR).mkdir(exist_ok=True)
Path(EXTRACT_DIR).mkdir(exist_ok=True)


@router.post("/upload")
async def upload_zip(file: UploadFile = File(...)):

    if not file.filename.endswith(".zip"):
        return {
            "success": False,
            "message": "Please upload a ZIP file."
        }

    zip_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extract_path = os.path.join(
        EXTRACT_DIR,
        file.filename.replace(".zip", "")
    )

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    return {
        "success": True,
        "message": "Repository uploaded successfully.",
        "repository": file.filename.replace(".zip", ""),
        "location": extract_path
    }