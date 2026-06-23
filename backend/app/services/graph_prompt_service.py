class GraphPromptService:

    @staticmethod
    def build_context(
        graph_results: list
    ) -> str:

        if not graph_results:
            return ""

        lines = []

        lines.append(
            "GRAPH CONTEXT:"
        )

        lines.append("")

        for item in graph_results:

            node = item.get(
                "node"
            )

            lines.append(
                f"Node: {node}"
            )

            neighbors = item.get(
                "neighbors",
                []
            )

            for neighbor in neighbors:

                relation = (
                    neighbor.get(
                        "relation"
                    )
                )

                target = (
                    neighbor.get(
                        "node"
                    )
                )

                lines.append(
                    f"  - {relation}: {target}"
                )

            lines.append("")

        return "\n".join(
            lines
        )