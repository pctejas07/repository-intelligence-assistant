import ast
from pathlib import Path


class PythonParser:

    @staticmethod
    def parse(
        file_path: str
    ):

        file_path = Path(file_path)

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            source_code = file.read()

        tree = ast.parse(
            source_code
        )

        result = {
            "imports": [],
            "classes": [],
            "functions": []
        }

        for node in tree.body:

            if isinstance(
                node,
                ast.Import
            ):

                for alias in node.names:

                    result["imports"].append(
                        alias.name
                    )

            elif isinstance(
                node,
                ast.ImportFrom
            ):

                if node.module:

                    result["imports"].append(
                        node.module
                    )

            elif isinstance(
                node,
                ast.ClassDef
            ):

                class_info = {
                    "name": node.name,
                    "bases": [],
                    "methods": []
                }

                for base in node.bases:

                    if hasattr(
                        base,
                        "id"
                    ):

                        class_info[
                            "bases"
                        ].append(
                            base.id
                        )

                for child in node.body:

                    if isinstance(
                        child,
                        ast.FunctionDef
                    ):

                        class_info[
                            "methods"
                        ].append(
                            {
                                "name":
                                child.name,

                                "calls":
                                PythonParser
                                ._extract_calls(
                                    child
                                )
                            }
                        )

                result[
                    "classes"
                ].append(
                    class_info
                )

            elif isinstance(
                node,
                ast.FunctionDef
            ):

                result[
                    "functions"
                ].append(
                    {
                        "name":
                        node.name
                    }
                )

        return result
    
    @staticmethod
    def _extract_calls(
        function_node
    ):

        calls = []

        for node in ast.walk(
            function_node
        ):

            if isinstance(
                node,
                ast.Call
            ):

                if isinstance(
                    node.func,
                    ast.Attribute
                ):

                    calls.append(
                        node.func.attr
                    )

                elif isinstance(
                    node.func,
                    ast.Name
                ):

                    calls.append(
                        node.func.id
                    )

        return list(
            set(calls)
        )