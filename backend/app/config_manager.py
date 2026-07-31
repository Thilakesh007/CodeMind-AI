import json
import os
from pydantic import BaseModel

CONFIG_FILE = "config.json"

class AppConfig(BaseModel):
    ollama_host: str = "http://localhost:11434"
    primary_model: str = "qwen2.5-coder"
    ai_provider: str = "ollama"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""

def load_config() -> AppConfig:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return AppConfig(**data)
        except Exception as e:
            print(f"Error loading config: {e}")
    
    # Return default if not exists or error
    return AppConfig()

def save_config(config: AppConfig) -> bool:
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config.dict(), f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False
