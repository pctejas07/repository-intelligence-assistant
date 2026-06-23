from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class ImpactAnalysisService:

    @staticmethod
    def analyze_impact(
        repository_name: str,
        node_name: str
    ):

        graph = (
            GraphStorageService.load_graph(
                repository_name
            )
        )

        if graph is None:

            return {
                "error": "Graph not found"
            }

        impacted_nodes = set()

        stack = [node_name]

        while stack:

            current = stack.pop()

            for child, _, data in graph.in_edges(
                current,
                data=True
            ):

                relation = data.get(
                    "relation"
                )

                if relation in [
                    "extends",
                    "implements"
                ]:

                    if child not in impacted_nodes:

                        impacted_nodes.add(
                            child
                        )

                        stack.append(
                            child
                        )

        return {
            "changed_node": node_name,
            "impacted_nodes":
            sorted(
                impacted_nodes
            ),
            "count":
            len(
                impacted_nodes
            )
        }