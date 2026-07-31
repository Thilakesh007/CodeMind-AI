from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.chat_history_manager import get_all_chats, get_chat, save_chat, delete_chat

router = APIRouter(prefix="/history", tags=["Chat History"])

class SaveChatRequest(BaseModel):
    chat_id: Optional[str] = None
    title: Optional[str] = None
    messages: List[Dict[str, Any]]

@router.get("/")
def list_history():
    return {"chats": get_all_chats()}

@router.get("/{chat_id}")
def get_single_history(chat_id: str):
    chat = get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/")
def create_or_update_history(request: SaveChatRequest):
    try:
        new_id = save_chat(request.chat_id, request.title, request.messages)
        return {"success": True, "chat_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{chat_id}")
def remove_history(chat_id: str):
    success = delete_chat(chat_id)
    if success:
        return {"success": True}
    raise HTTPException(status_code=404, detail="Chat not found")
