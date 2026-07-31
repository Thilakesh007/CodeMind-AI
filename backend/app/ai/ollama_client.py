import ollama


import os

from app.config_manager import load_config

def generate_response(prompt: str, history: list = None, stream: bool = False):
    config = load_config()
    
    # Check if a custom host is configured (useful for Docker)
    host = os.environ.get("OLLAMA_HOST", config.ollama_host)
    client = ollama.Client(host=host)
    
    model_name = config.primary_model

    messages = []
    if history:
        for msg in history:
            # ensure we only pass role and content
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
    
    messages.append({
        "role": "user",
        "content": prompt
    })

    if stream:
        response = client.chat(
            model=model_name,
            messages=messages,
            stream=True
        )
        for chunk in response:
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
    else:
        response = client.chat(
            model=model_name,
            messages=messages,
            stream=False
        )
        return response["message"]["content"]