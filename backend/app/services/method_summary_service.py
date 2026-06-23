from app.services.graph.call_analysis_service import (
    CallAnalysisService
)


class MethodSummaryService:

    @staticmethod
    def summarize_method(
        repository_name: str,
        method_name: str
    ):

        callees = (
            CallAnalysisService
            .get_callees(
                repository_name,
                method_name
            )
        )

        callers = (
            CallAnalysisService
            .get_callers(
                repository_name,
                method_name
            )
        )

        call_chain = (
            CallAnalysisService
            .get_call_chain(
                repository_name,
                method_name
            )
        )

        return {
            "method":
            method_name,

            "callees":
            callees.get(
                "callees",
                []
            ),

            "callers":
            callers.get(
                "callers",
                []
            ),

            "call_chain":
            call_chain.get(
                "call_chain",
                []
            )
        }