from pydantic import BaseModel
from typing import Dict


class RepositoryStatsResponse(BaseModel):
    repository_name: str
    total_files: int
    total_chunks: int
    indexed_vectors: int
    languages: Dict[str, int]