from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.tree import router as tree_router
from app.api.index import router as index_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.review import router as review_router
from app.api.documentation import router as documentation_router
from app.api.architecture import router as architecture_router
from app.api.clone import router as clone_router
from app.api.projects import router as projects_router
from app.api.tests import router as tests_router
from app.api.readme import router as readme_router
from app.api.settings import router as settings_router
from app.api.history import router as history_router
from app.api.auth import router as auth_router

app = FastAPI(
    title="CodeMind AI",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(tree_router)
app.include_router(index_router)
app.include_router(chat_router)
app.include_router(review_router)
app.include_router(documentation_router)
app.include_router(architecture_router)
app.include_router(clone_router)
app.include_router(projects_router)
app.include_router(tests_router)
app.include_router(readme_router)
app.include_router(settings_router)
app.include_router(history_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CodeMind AI 🚀"
    }
