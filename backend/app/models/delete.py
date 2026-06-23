from pydantic import BaseModel


class DeleteRepositoryResponse(
    BaseModel
):
    repository_name: str
    deleted_vectors: int
    status: str