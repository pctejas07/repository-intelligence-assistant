from app.services.repository_service import RepositoryService
from app.services.code_chunker import CodeChunker



class ChunkService:

    @staticmethod
    def chunk_repository(
        repository_name: str
    ):

        scan_result = (
            RepositoryService.scan_repository(
                repository_name
            )
        )

        all_chunks = []

        for file_info in scan_result["files"]:

            chunks = (
                CodeChunker.chunk_file(
                    file_info["file_path"],
                    file_info["language"]
                )
            )

            all_chunks.extend(chunks)

        return {
            "repository_name": repository_name,
            "total_chunks": len(all_chunks),
            "chunks": all_chunks
        }