from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class HierarchyAnalysisService:

    @staticmethod
    def get_parent_classes(
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

        parents = []

        for _, target, data in graph.out_edges(
            class_name,
            data=True
        ):

            if (
                data.get("relation")
                == "extends"
            ):

                parents.append(
                    target
                )

        return {
            "class": class_name,
            "extends": parents
        }

    @staticmethod
    def get_child_classes(
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

        children = []

        for source, _, data in graph.in_edges(
            class_name,
            data=True
        ):

            if (
                data.get("relation")
                == "extends"
            ):

                children.append(
                    source
                )

        return {
            "class": class_name,
            "children": children
        }

    @staticmethod
    def get_interfaces(
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

        interfaces = []

        for _, target, data in graph.out_edges(
            class_name,
            data=True
        ):

            if (
                data.get("relation")
                == "implements"
            ):

                interfaces.append(
                    target
                )

        return {
            "class": class_name,
            "interfaces": interfaces
        }