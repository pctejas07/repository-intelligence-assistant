from pydantic import BaseModel
from typing import Dict, List


class FileInfo(BaseModel):
    file_name: str
    file_path: str
    language: str


class ScanResponse(BaseModel):
    repository_path: str
    total_supported_files: int
    language_breakdown: Dict[str, int]
    files: List[FileInfo]