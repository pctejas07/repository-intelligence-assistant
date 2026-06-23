from app.services.graph.graph_storage_service import (
    GraphStorageService
)

from app.services.graph.graph_service import (
    GraphService
)


class DependencyAnalysisService:

    @staticmethod
    def get_dependencies(
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
                "error":
                "Graph not found"
            }

        dependencies = (
            GraphService.get_dependencies(
                graph,
                node_name
            )
        )

        return {
            "node": node_name,
            "dependencies":
            dependencies,
            "count":
            len(dependencies)
        }

    @staticmethod
    def get_dependents(
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
                "error":
                "Graph not found"
            }

        dependents = (
            GraphService.get_dependents(
                graph,
                node_name
            )
        )

        return {
            "node": node_name,
            "dependents":
            dependents,
            "count":
            len(dependents)
        }