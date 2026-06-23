class GraphAnswerService:

    @staticmethod
    def build_context(
        question_type: str,
        graph_result: dict
    ):

        method_name = (
            graph_result.get(
                "method",
                ""
            )
        )

        lines = []

        if question_type == "callers":

            lines.append(
                f"Method: {method_name}"
            )

            lines.append(
                "Methods that call it:"
            )

            for caller in (
                graph_result.get(
                    "callers",
                    []
                )
            ):

                lines.append(
                    f"- {caller}"
                )

        elif question_type == "callees":

            lines.append(
                f"Method: {method_name}"
            )

            lines.append(
                "Methods it calls:"
            )

            for callee in (
                graph_result.get(
                    "callees",
                    []
                )
            ):

                lines.append(
                    f"- {callee}"
                )

        elif question_type == "impact":

            lines.append(
                f"Method: {method_name}"
            )

            lines.append(
                "Impacted methods:"
            )

            for impacted in (
                graph_result.get(
                    "impacted_methods",
                    []
                )
            ):

                lines.append(
                    f"- {impacted}"
                )

        elif question_type == "call_chain":

            lines.append(
                f"Method: {method_name}"
            )

            lines.append(
                "Call chain:"
            )

            for node in (
                graph_result.get(
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