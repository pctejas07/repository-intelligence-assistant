from fastapi import APIRouter

from app.services.github_service import GitHubService
from app.services.repository_service import RepositoryService
from app.services.chunk_service import ChunkService
from app.services.indexing_service import IndexingService
from app.services.search_service import SearchService
from app.services.chat_service import ChatService

from app.models.chat import (
    ChatRequest,
    ChatResponse
)

from app.models.repository import (
    RepositoryRequest,
    RepositoryResponse
)

from app.models.scanner import ScanResponse
from app.models.chunk import ChunkResponse
from app.models.indexing import IndexingResponse

from app.models.search import (
    SearchRequest,
    SearchResponse
)
from app.models.delete import (
    DeleteRepositoryResponse
)
from app.models.stats import (
    RepositoryStatsResponse
)

router = APIRouter(
    prefix="/repository",
    tags=["Repository"]
)


@router.post(
    "/clone",
    response_model=RepositoryResponse
)
def clone_repository(
    request: RepositoryRequest
):
    return GitHubService.clone_repository(
        request.github_url
    )


@router.get(
    "/scan",
    response_model=ScanResponse
)
def scan_repository(
    repository_name: str
):
    return RepositoryService.scan_repository(
        repository_name
    )


@router.get(
    "/chunks",
    response_model=ChunkResponse
)
def get_repository_chunks(
    repository_name: str
):
    return ChunkService.chunk_repository(
        repository_name
    )


@router.post(
    "/index",
    response_model=IndexingResponse
)
def index_repository(
    repository_name: str
):
    return (
        IndexingService.index_repository(
            repository_name
        )
    )


@router.post(
    "/search",
    response_model=SearchResponse
)
def search_repository(
    request: SearchRequest
):
    return SearchService.semantic_search(
        repository_name=request.repository_name,
        query=request.query,
        top_k=request.top_k
    )


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat_repository(
    request: ChatRequest
):
    return ChatService.ask_repository(
        repository_name=request.repository_name,
        question=request.question,
        top_k=request.top_k
    )

@router.delete(
    "/{repository_name}",
    response_model=DeleteRepositoryResponse
)
def delete_repository(
    repository_name: str
):

    return (
        RepositoryService.delete_repository(
            repository_name
        )
    )

@router.get(
    "/stats",
    response_model=RepositoryStatsResponse
)
def get_repository_stats(
    repository_name: str
):

    return (
        RepositoryService.get_repository_stats(
            repository_name
        )
    )