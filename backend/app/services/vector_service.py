import chromadb

from app.core.config import settings


class VectorService:

    COLLECTION_NAME = "code_chunks"

    _client = None
    _collection = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = chromadb.PersistentClient(
                path=str(settings.CHROMA_DB_PATH)
            )

        return cls._client

    @classmethod
    def get_collection(cls):

        if cls._collection is None:

            client = cls.get_client()

            cls._collection = client.get_or_create_collection(
                name=cls.COLLECTION_NAME
            )

        return cls._collection

    @classmethod
    def add_chunks(
        cls,
        ids,
        embeddings,
        documents,
        metadatas
    ):

        collection = cls.get_collection()

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    @classmethod
    def search(
        cls,
        query_embedding,
        top_k=5
    ):

        collection = cls.get_collection()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    @classmethod
    def search_by_repository(
        cls,
        query_embedding,
        repository_name: str,
        top_k: int = 5
    ):

        collection = cls.get_collection()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={
                "repository": repository_name
            }
        )

        return results

    @classmethod
    def delete_repository_chunks(
        cls,
        repository_name: str
    ):

        collection = cls.get_collection()

        existing = collection.get(
            where={
                "repository": repository_name
            }
        )

        deleted_count = len(
            existing.get(
                "ids",
                []
            )
        )

        if deleted_count > 0:

            collection.delete(
                where={
                    "repository": repository_name
                }
            )

        return deleted_count

    @classmethod
    def count_repository_chunks(
        cls,
        repository_name: str
    ):

        collection = cls.get_collection()

        results = collection.get(
            where={
                "repository": repository_name
            }
        )

        return len(
            results.get(
                "ids",
                []
            )
        )