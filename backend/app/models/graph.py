from pydantic import BaseModel
from typing import Optional


class GraphNode(BaseModel):

    id: str

    node_type: str

    name: str

    language: Optional[str] = None

    file_path: Optional[str] = None


class GraphEdge(BaseModel):

    source: str

    target: str

    relation: str


class GraphBuildResponse(BaseModel):

    repository_name: str

    total_nodes: int

    total_edges: int