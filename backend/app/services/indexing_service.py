import hashlib


from app.core.logger import logger

from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

from app.services.graph.graph_service import (
    GraphService
)

from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class IndexingService:

    @staticmethod
    def generate_chunk_id(
        repository_name: str,
        file_path: str,
        chunk_name: str,
        chunk_content: str
    ) -> str:

        unique_string = (
            f"{repository_name}:"
            f"{file_path}:"
            f"{chunk_name}:"
            f"{chunk_content}"
        )

        return hashlib.md5(
            unique_string.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def index_repository(
        repository_name: str
    ):

        logger.info(
            f"Indexing repository: {repository_name}"
        )

        chunk_result = (
            ChunkService.chunk_repository(
                repository_name
            )
        )

        chunks = chunk_result["chunks"]

        if not chunks:

            return {
                "repository_name": repository_name,
                "indexed_chunks": 0,
                "status": "indexed"
            }

        # ----------------------------------
        # Build & Save Graph
        # ----------------------------------

        logger.info(
            f"Building graph for "
            f"{repository_name}"
        )

        graph = (
            GraphService.build_graph(
                chunks
            )
        )

        GraphStorageService.save_graph(
            repository_name,
            graph
        )

        logger.info(
            f"Graph saved for "
            f"{repository_name} "
            f"with "
            f"{graph.number_of_nodes()} nodes "
            f"and "
            f"{graph.number_of_edges()} edges"
        )

        # ----------------------------------
        # Vector Indexing
        # ----------------------------------

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            chunk_id = (
                IndexingService.generate_chunk_id(
                    repository_name,
                    chunk.file_path,
                    chunk.name,
                    chunk.content
                )
            )

            if chunk_id in ids:

                logger.warning(
                f"DUPLICATE: "
                f"{chunk.file_path} "
                f"{chunk.name}"
            )

            ids.append(
                chunk_id
            )

            documents.append(
                chunk.content
            )

            metadatas.append(
                {
                    "repository": repository_name,
                    "chunk_type": chunk.chunk_type,
                    "name": chunk.name,
                    "file_path": chunk.file_path,
                    "language": chunk.language
                }
            )

        logger.info(
            f"Removing existing vectors "
            f"for {repository_name}"
        )

        VectorService.delete_repository_chunks(
            repository_name
        )

        embeddings = (
            EmbeddingService.generate_embeddings(
                documents
            )
        )
        
        VectorService.add_chunks(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        logger.info(
            f"Indexed {len(chunks)} chunks "
            f"for {repository_name}"
        )

        return {
            "repository_name": repository_name,
            "indexed_chunks": len(chunks),
            "graph_nodes": graph.number_of_nodes(),
            "graph_edges": graph.number_of_edges(),
            "status": "indexed"
        }