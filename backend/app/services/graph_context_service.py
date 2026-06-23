from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class GraphContextService:

    @staticmethod
    def expand_node(
        repository_name: str,
        node_name: str,
        max_neighbors: int = 20
    ):

        graph = (
            GraphStorageService.load_graph(
                repository_name
            )
        )

        if graph is None:

            return {
                "error":
                "Graph not found"
            }

        if node_name not in graph:

            return {
                "node": node_name,
                "neighbors": []
            }

        neighbors = []

        # outgoing edges

        for _, target, data in graph.out_edges(
            node_name,
            data=True
        ):

            neighbors.append(
                {
                    "relation":
                    data.get(
                        "relation"
                    ),
                    "node":
                    target
                }
            )

        # incoming edges

        for source, _, data in graph.in_edges(
            node_name,
            data=True
        ):

            neighbors.append(
                {
                    "relation":
                    data.get(
                        "relation"
                    ),
                    "node":
                    source
                }
            )


        filtered_neighbors = []

        for neighbor in neighbors:

            relation = neighbor.get(
                "relation"
            )

#            if relation == "imports":
#                continue

            filtered_neighbors.append(
                neighbor
            )

        priority_relations = [
            "extends",
            "implements",
            "contains",
            "calls"
        ]

        sorted_neighbors = sorted(
            filtered_neighbors,
            key=lambda x:
            (
                x["relation"]
                not in priority_relations
            )
        )

        return {
            "node": node_name,
            "neighbor_count":
            len(sorted_neighbors),
            "neighbors":
            sorted_neighbors[:max_neighbors]
        }

        