from fastapi import FastAPI

from app.api.repository import router as repository_router
from app.core.exceptions import (
    RepositoryNotFoundException,
    repository_not_found_handler,
    generic_exception_handler
)
from app.api.graph import (
    router as graph_router
)

app = FastAPI(
    title="Repository Intelligence Assistant",
    version="1.0.0",
    description="Advanced GraphRAG-based GitHub Repository Assistant"
)

app.add_exception_handler(
    RepositoryNotFoundException,
    repository_not_found_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

@app.get("/")
def home():
    return {
        "message": "GitHub Codebase Assistant Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(repository_router)

app.include_router(graph_router)