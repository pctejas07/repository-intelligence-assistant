from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    repository_name: str
    question: str
    top_k: int = 5


class SourceReference(BaseModel):
    file_path: str
    chunk_name: str
    chunk_type: str


class ChatResponse(BaseModel):
    repository_name: str
    question: str
    answer: str
    sources: List[SourceReference]