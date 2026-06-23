from app.services.graph_context_service import (
    GraphContextService
)


class GraphSummaryService:

    @staticmethod
    def summarize_node(
        repository_name: str,
        node_name: str
    ):

        graph_context = (
            GraphContextService
            .expand_node(
                repository_name,
                node_name,
                max_neighbors=100
            )
        )

        parent_classes = []
        interfaces = []
        methods = []
        dependencies = []

        for neighbor in (
            graph_context.get(
                "neighbors",
                []
            )
        ):

            relation = (
                neighbor.get(
                    "relation"
                )
            )

            node = (
                neighbor.get(
                    "node"
                )
            )

            if relation == "extends":

                parent_classes.append(
                    node
                )

            elif relation == "implements":

                interfaces.append(
                    node
                )

            elif relation == "imports":

                dependencies.append(
                    node
                )

            elif relation == "contains":

                methods.append(
                    node
                )

        return {
            "node": node_name,
            "parent_classes":
            parent_classes,
            "interfaces":
            interfaces,
            "dependencies":
            dependencies,
            "methods":
            methods
        }