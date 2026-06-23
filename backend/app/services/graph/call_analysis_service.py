from app.services.graph.graph_storage_service import (
    GraphStorageService
)


class CallAnalysisService:

    @staticmethod
    def get_callees(
        repository_name: str,
        method_name: str
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

        callees = []

        for _, target, data in graph.out_edges(
            method_name,
            data=True
        ):

            if (
                data.get("relation")
                == "calls"
            ):

                callees.append(
                    target
                )

        return {
            "method":
            method_name,
            "callees":
            callees
        }
    
    @staticmethod
    def get_callers(
        repository_name: str,
        method_name: str
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

        callers = []

        for source, _, data in graph.in_edges(
            method_name,
            data=True
        ):

            if (
                data.get("relation")
                == "calls"
            ):

                callers.append(
                    source
                )

        return {
            "method":
            method_name,
            "callers":
            callers
        }
    
    @staticmethod
    def get_impacted_methods(
        repository_name: str,
        method_name: str
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

        impacted = set()

        stack = [method_name]

        while stack:

            current = stack.pop()

            for source, _, data in graph.in_edges(
                current,
                data=True
            ):

                if (
                    data.get("relation")
                    != "calls"
                ):
                    continue

                if source in impacted:
                    continue

                impacted.add(
                    source
                )

                stack.append(
                    source
                )

        return {
            "method":
            method_name,
            "impacted_methods":
            sorted(
                impacted
            )
        }
    
    @staticmethod
    def get_call_chain(
        repository_name: str,
        method_name: str
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

        chain = []

        visited = set()

        def dfs(node):

            if node in visited:
                return

            visited.add(node)

            chain.append(node)

            for _, target, data in graph.out_edges(
                node,
                data=True
            ):

                if (
                    data.get("relation")
                    == "calls"
                ):

                    dfs(target)

        dfs(method_name)

        return {
            "method": method_name,
            "call_chain": chain
        }