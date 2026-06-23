from pydantic import BaseModel
from typing import List


class SearchRequest(BaseModel):
    repository_name: str
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    chunk_name: str
    chunk_type: str
    file_path: str
    language: str
    content: str


class SearchResponse(BaseModel):
    repository_name: str
    query: str
    total_results: int
    results: List[SearchResult]