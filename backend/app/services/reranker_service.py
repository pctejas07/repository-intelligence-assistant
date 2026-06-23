from sentence_transformers import CrossEncoder


class RerankerService:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

        return cls._model

    @classmethod
    def rerank(
        cls,
        query: str,
        results: list,
        top_k: int = 5
    ):

        if not results:
            return []

        model = cls.get_model()

        pairs = [
            (
                query,
                item["content"]
            )
            for item in results
        ]

        scores = model.predict(
            pairs
        )

        ranked = sorted(
            zip(results, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            item
            for item, score in ranked[:top_k]
        ]