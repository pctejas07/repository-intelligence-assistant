from pathlib import Path

from tree_sitter import Language
from tree_sitter import Parser

import tree_sitter_java as tsjava


class JavaParser:

    @staticmethod
    def _get_parser():

        java_language = Language(
            tsjava.language()
        )

        parser = Parser(
            java_language
        )

        return parser

    @staticmethod
    def parse(
        file_path: str
    ):

        file_path = Path(file_path)

        source_code = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        parser = JavaParser._get_parser()

        tree = parser.parse(
            bytes(
                source_code,
                "utf8"
            )
        )

        root = tree.root_node

        result = {
            "package": None,
            "imports": [],
            "classes": []
        }

        JavaParser._extract_package(
            root,
            source_code,
            result
        )

        JavaParser._extract_imports(
            root,
            source_code,
            result
        )

        JavaParser._extract_classes(
            root,
            source_code,
            result
        )

        return result

    @staticmethod
    def _extract_package(
        root,
        source_code,
        result
    ):

        for child in root.children:

            if child.type == (
                "package_declaration"
            ):

                result[
                    "package"
                ] = source_code[
                    child.start_byte:
                    child.end_byte
                ]

    @staticmethod
    def _extract_imports(
        root,
        source_code,
        result
    ):

        for child in root.children:

            if child.type == (
                "import_declaration"
            ):

                import_text = (
                    source_code[
                        child.start_byte:
                        child.end_byte
                    ]
                )

                import_text = (
                    import_text
                    .replace("import", "")
                    .replace(";", "")
                    .strip()
                )

                result[
                    "imports"
                ].append(
                    import_text
                )

    @staticmethod
    def _extract_classes(
        root,
        source_code,
        result
    ):

        stack = [root]

        while stack:

            node = stack.pop()

            if node.type in [
                "class_declaration",
                "interface_declaration"
            ]:

                class_info = {
                    "type": (
                        "interface"
                        if node.type
                        == "interface_declaration"
                        else "class"
                    ),

                    "name": None,

                    "extends": None,

                    "implements": [],

                    "methods": []
                }
                for child in node.children:

                    if (
                        child.type
                        == "identifier"
                    ):

                        if (
                            class_info["name"]
                            is None
                        ):

                            class_info[
                                "name"
                            ] = source_code[
                                child.start_byte:
                                child.end_byte
                            ]

                    elif (
                        child.type
                        == "superclass"
                    ):

                        for subchild in (
                            child.children
                        ):

                            if (
                                subchild.type
                                == "type_identifier"
                            ):

                                class_info[
                                    "extends"
                                ] = source_code[
                                    subchild.start_byte:
                                    subchild.end_byte
                                ]

                    elif (
                        child.type
                        == "super_interfaces"
                    ):

                        for subchild in (
                            child.children
                        ):

                            if (
                                subchild.type
                                == "type_list"
                            ):

                                interface_name = (
                                    source_code[
                                        subchild.start_byte:
                                        subchild.end_byte
                                    ]
                                    .strip()
                                )

                                class_info[
                                    "implements"
                                ].append(
                                    interface_name
                                )

                body = next(
                    (
                        c
                        for c in node.children
                        if c.type
                        == "class_body"
                    ),
                    None
                )

                if body:

                    for body_child in (
                        body.children
                    ):

                        if (
                            body_child.type
                            == "method_declaration"
                        ):

                            method_name = (
                                JavaParser
                                ._extract_method_name(
                                    body_child,
                                    source_code
                                )
                            )


                            method_calls = (
                                JavaParser
                                ._extract_method_calls(
                                    body_child,
                                    source_code
                                )
                            )

                            class_info[
                                "methods"
                            ].append(
                                {
                                    "name":
                                    method_name,

                                    "calls":
                                    method_calls
                                }
                            )


                result[
                    "classes"
                ].append(
                    class_info
                )

            stack.extend(
                reversed(
                    node.children
                )
            )

    @staticmethod
    def _extract_method_name(
        method_node,
        source_code
    ):

        for child in (
            method_node.children
        ):

            if (
                child.type
                == "identifier"
            ):

                return source_code[
                    child.start_byte:
                    child.end_byte
                ]

        return None
    
    
    @staticmethod
    def _extract_method_calls(
        method_node,
        source_code
    ):

        calls = []

        stack = [method_node]

        while stack:

            node = stack.pop()

            if (
                node.type
                == "method_invocation"
            ):

                call_name = None

                for child in (
                    node.children
                ):

                    if (
                        child.type
                        == "identifier"
                    ):

                        call_name = source_code[
                            child.start_byte:
                            child.end_byte
                        ]

                        break

                if call_name:

                    calls.append(
                        call_name
                    )

            stack.extend(
                reversed(
                    node.children
                )
            )

        return list(
            set(calls)
        )