from app.services.graph_context_service import (
    GraphContextService
)
from app.core.logger import logger

class GraphRetrievalService:

    @staticmethod
    def expand_search_results(
        repository_name: str,
        search_results: list,
        max_neighbors: int = 25
    ):

        expanded_context = []

        visited = set()

        for result in search_results:

            if result.get("chunk_type") != "class":
                continue

            node_name = (
                result.get(
                    "chunk_name"
                )
            )
            logger.info(
                f"GRAPH NODE: "
                f"{node_name}"
            )

            if not node_name:
                continue

            if node_name in visited:
                continue

            visited.add(
                node_name
            )

            graph_context = (
                GraphContextService
                .expand_node(
                    repository_name,
                    node_name,
                    max_neighbors
                )
            )

            neighbors = (
                graph_context.get(
                    "neighbors",
                    []
                )
            )

            if not neighbors:
                continue

            expanded_context.append(
                {
                    "node": node_name,
                    "neighbors": neighbors
                }
            )

        return expanded_context