from pathlib import Path

import os
import stat
import shutil

from app.core.config import settings
from app.core.exceptions import (
    RepositoryNotFoundException
)

from app.services.repository_scanner import RepositoryScanner

from app.core.logger import logger
from app.services.vector_service import (
    VectorService
)


class RepositoryService:

    @staticmethod
    def get_repository_path(repository_name: str) -> Path:

        repo_path = settings.REPOSITORY_PATH / repository_name

        if not repo_path.exists():
            raise RepositoryNotFoundException(
                repository_name
            )

        return repo_path

    @staticmethod
    def remove_readonly(
        func,
        path,
        _
    ):
        os.chmod(
            path,
            stat.S_IWRITE
        )
        func(path)

    @staticmethod
    def scan_repository(repository_name: str) -> dict:

        repo_path = RepositoryService.get_repository_path(
            repository_name
        )

        return RepositoryScanner.scan_repository(
            str(repo_path)
        )

    @staticmethod
    def delete_repository(
        repository_name: str
    ):

        repo_path = (
            RepositoryService.get_repository_path(
                repository_name
            )
        )
        logger.info(
            f"Starting repository deletion: "
            f"{repository_name}"
        )

        deleted_vectors = (
            VectorService.delete_repository_chunks(
                repository_name
            )
        )
        logger.info(
            f"Deleted {deleted_vectors} vectors "
            f"for {repository_name}"
        )

        shutil.rmtree(
            repo_path,
            onerror=RepositoryService.remove_readonly
        )

        logger.info(
            f"Deleted repository: "
            f"{repository_name}"
        )

        return {
            "repository_name": repository_name,
            "deleted_vectors": deleted_vectors,
            "status": "deleted"
        }
    
    @staticmethod
    def get_repository_stats(
        repository_name: str
    ):
        from app.services.chunk_service import ChunkService
        scan_result = (
            RepositoryService.scan_repository(
                repository_name
            )
        )

        chunk_result = (
            ChunkService.chunk_repository(
                repository_name
            )
        )

        indexed_vectors = (
            VectorService.count_repository_chunks(
                repository_name
            )
        )

        return {
            "repository_name": repository_name,
            "total_files": scan_result[
                "total_supported_files"
            ],
            "total_chunks": chunk_result[
                "total_chunks"
            ],
            "indexed_vectors": indexed_vectors,
            "languages": scan_result[
                "language_breakdown"
            ]
        }