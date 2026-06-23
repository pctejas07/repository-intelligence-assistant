from pydantic import BaseModel


class RepositoryRequest(BaseModel):
    github_url: str


class RepositoryResponse(BaseModel):
    status: str
    repository_name: str
    repository_path: str