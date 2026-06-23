from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class SearchService:

    @staticmethod
    def semantic_search(
        repository_name: str,
        query: str,
        top_k: int = 5
    ):

        query_embedding = (
            EmbeddingService.generate_embedding(
                query
            )
        )

        results = (
            VectorService.search_by_repository(
                query_embedding=query_embedding,
                repository_name=repository_name,
                top_k=top_k
            )
        )

        formatted_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for document, metadata in zip(
            documents,
            metadatas
        ):

            formatted_results.append(
                {
                    "chunk_name": metadata["name"],
                    "chunk_type": metadata["chunk_type"],
                    "file_path": metadata["file_path"],
                    "language": metadata["language"],
                    "content": document
                }
            )

        return {
            "repository_name": repository_name,
            "query": query,
            "total_results": len(
                formatted_results
            ),
            "results": formatted_results
        }