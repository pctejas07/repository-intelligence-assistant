from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class MethodDiscoveryService:

    @staticmethod
    def get_methods(
        repository_name: str,
        class_name: str
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

        methods = []

        for _, target, data in graph.out_edges(
            class_name,
            data=True
        ):

            if (
                data.get("relation")
                == "contains"
            ):

                methods.append(
                    target
                )

        methods.sort()

        return {
            "class": class_name,
            "methods": methods,
            "count": len(methods)
        }