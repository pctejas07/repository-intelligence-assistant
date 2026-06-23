from pydantic import BaseModel


class IndexingResponse(BaseModel):
    repository_name: str
    indexed_chunks: int
    status: str