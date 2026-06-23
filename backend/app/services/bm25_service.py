from rank_bm25 import BM25Okapi


class BM25Service:

    @staticmethod
    def search(
        query: str,
        documents: list[str],
        top_k: int = 5
    ):

        tokenized_docs = [
            doc.lower().split()
            for doc in documents
        ]

        bm25 = BM25Okapi(
            tokenized_docs
        )

        scores = bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]