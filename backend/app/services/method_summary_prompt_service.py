class MethodSummaryPromptService:

    @staticmethod
    def build_context(
        summary: dict
    ):

        lines = []

        lines.append(
            "METHOD SUMMARY"
        )

        lines.append("")

        lines.append(
            f"Method: "
            f"{summary['method']}"
        )

        lines.append("")

        lines.append(
            "Calls:"
        )

        for callee in (
            summary.get(
                "callees",
                []
            )
        ):

            lines.append(
                f"- {callee}"
            )

        lines.append("")

        lines.append(
            "Called By:"
        )

        for caller in (
            summary.get(
                "callers",
                []
            )
        ):

            lines.append(
                f"- {caller}"
            )

        lines.append("")

        lines.append(
            "Call Chain:"
        )

        for node in (
            summary.get(
                "call_chain",
                []
            )
        ):

            lines.append(
                f"- {node}"
            )

        return "\n".join(
            lines
        )