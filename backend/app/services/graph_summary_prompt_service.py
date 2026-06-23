class GraphSummaryPromptService:

    @staticmethod
    def build_context(
        summary: dict
    ):

        lines = []

        lines.append(
            "CLASS SUMMARY"
        )

        lines.append(
            ""
        )

        lines.append(
            f"Class: "
            f"{summary['node']}"
        )

        lines.append(
            ""
        )

        lines.append(
            "Parent Classes:"
        )

        lines.append(
            ""
        )

        lines.append(
            "Interfaces:"
        )

        for interface in (
            summary.get(
                "interfaces",
                []
            )
        ):

            lines.append(
                f"- {interface}"
            )

        lines.append(
            ""
        )

        lines.append(
            "Dependencies:"
        )

        for dependency in (
            summary.get(
                "dependencies",
                []
            )
        ):

            lines.append(
                f"- {dependency}"
            )

        for parent in (
            summary.get(
                "parent_classes",
                []
            )
        ):

            lines.append(
                f"- {parent}"
            )

        lines.append(
            ""
        )

        lines.append(
            "Methods:"
        )

        for method in (
            summary.get(
                "methods",
                []
            )
        ):

            lines.append(
                f"- {method}"
            )

        return "\n".join(
            lines
        )