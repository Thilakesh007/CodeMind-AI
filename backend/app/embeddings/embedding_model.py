import os
import httpx
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{MODEL_ID}"

def generate_embeddings(texts):
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN environment variable is missing. Please set it in your .env or Render dashboard.")
        
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Send the texts to HuggingFace
    response = httpx.post(
        API_URL, 
        headers=headers, 
        json={"inputs": texts, "options": {"wait_for_model": True}},
        timeout=60.0
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch embeddings from HuggingFace: {response.text}")
        
    return response.json()