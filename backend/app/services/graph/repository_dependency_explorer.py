from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class RepositoryDependencyExplorer:

    @staticmethod
    def explore(
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

        outgoing = []

        for _, target, data in graph.out_edges(
            node_name,
            data=True
        ):

            outgoing.append(
                {
                    "relation":
                    data.get(
                        "relation"
                    ),
                    "target":
                    target
                }
            )

        incoming = []

        for source, _, data in graph.in_edges(
            node_name,
            data=True
        ):

            incoming.append(
                {
                    "relation":
                    data.get(
                        "relation"
                    ),
                    "source":
                    source
                }
            )

        return {
            "node": node_name,
            "outgoing": outgoing,
            "incoming": incoming,
            "outgoing_count":
            len(outgoing),
            "incoming_count":
            len(incoming)
        }