from pydantic import BaseModel
from typing import List, Optional


class CodeChunk(BaseModel):

    chunk_type: str
    name: str
    content: str

    file_path: str
    language: str

    package_name: Optional[str] = None

    imports: List[str] = []

    parent_class: Optional[str] = None

    extends: Optional[str] = None

    implements: List[str] = []

    calls: List[str] = []


class ChunkResponse(BaseModel):

    repository_name: str
    total_chunks: int
    chunks: List[CodeChunk]