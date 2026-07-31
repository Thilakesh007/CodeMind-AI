import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

HISTORY_FILE = "chat_histories.json"

def load_histories() -> Dict[str, Any]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading chat histories: {e}")
    return {}

def save_histories(histories: Dict[str, Any]):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(histories, f, indent=4)
    except Exception as e:
        print(f"Error saving chat histories: {e}")

def get_all_chats() -> List[Dict[str, Any]]:
    histories = load_histories()
    # Return list of chats sorted by updated_at descending
    chats = list(histories.values())
    chats.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    
    # Don't return full messages for the list view to save bandwidth
    return [{
        "id": c["id"],
        "title": c.get("title", "New Chat"),
        "updated_at": c.get("updated_at", "")
    } for c in chats]

def get_chat(chat_id: str) -> Dict[str, Any]:
    histories = load_histories()
    return histories.get(chat_id)

def save_chat(chat_id: str, title: str, messages: List[Dict[str, Any]]) -> str:
    histories = load_histories()
    
    if not chat_id:
        chat_id = str(uuid.uuid4())
    
    # Auto-generate title from first user message if not provided
    if not title and messages:
        for msg in messages:
            if msg.get("role") == "user":
                title = msg.get("content", "")[:40] + "..."
                break
    if not title:
        title = "New Chat"
        
    histories[chat_id] = {
        "id": chat_id,
        "title": title,
        "messages": messages,
        "updated_at": datetime.now().isoformat()
    }
    save_histories(histories)
    return chat_id

def delete_chat(chat_id: str) -> bool:
    histories = load_histories()
    if chat_id in histories:
        del histories[chat_id]
        save_histories(histories)
        return True
    return False
