from fastapi import FastAPI

app = FastAPI(
    title="CodeMind AI",
    version="1.0.0",
    description="AI-powered Codebase Assistant"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to CodeMind AI 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "Running"
    }