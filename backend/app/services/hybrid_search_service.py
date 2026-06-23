from app.services.search_service import SearchService
from app.services.bm25_service import BM25Service
from app.services.vector_service import VectorService
from app.services.embedding_service import EmbeddingService


class HybridSearchService:

    @staticmethod
    def search(
        repository_name: str,
        query: str,
        top_k: int = 5
    ):

        # Vector Search
        vector_results = (
            SearchService.semantic_search(
                repository_name=repository_name,
                query=query,
                top_k=top_k
            )
        )

        # Load all repository chunks
        collection = (
            VectorService.get_collection()
        )

        repository_chunks = (
            collection.get(
                where={
                    "repository": repository_name
                }
            )
        )

        documents = (
            repository_chunks.get(
                "documents",
                []
            )
        )

        metadatas = (
            repository_chunks.get(
                "metadatas",
                []
            )
        )

        # BM25 Search
        bm25_results = (
            BM25Service.search(
                query=query,
                documents=documents,
                top_k=top_k
            )
        )

        combined_results = []

        # Add vector results
        for result in vector_results[
            "results"
        ]:

            combined_results.append(
                result
            )

        # Add BM25 results
        for document, score in bm25_results:

            for metadata, doc in zip(
                metadatas,
                documents
            ):

                if doc == document:

                    combined_results.append(
                        {
                            "chunk_name": metadata[
                                "name"
                            ],
                            "chunk_type": metadata[
                                "chunk_type"
                            ],
                            "file_path": metadata[
                                "file_path"
                            ],
                            "language": metadata[
                                "language"
                            ],
                            "content": doc
                        }
                    )

                    break

        # Remove duplicate chunks that appear in both Vector and BM25
 
        seen = set()

        final_results = []

        for result in combined_results:

            key = (
                result["file_path"],
                result["chunk_name"]
            )

            if key in seen:
                continue

            seen.add(key)

            final_results.append(
                result
            )

        return {
            "repository_name": repository_name,
            "query": query,
            "total_results": len(
                final_results[:top_k]
            ),
            "results": final_results[:top_k]
        }