from pathlib import Path

from app.models.chunk import (
    CodeChunk
)

from app.services.parsers.python_parser import (
    PythonParser
)


class PythonChunker:

    @staticmethod
    def chunk(
        file_path: str
    ):

        parsed = (
            PythonParser.parse(
                file_path
            )
        )

        file_path_obj = (
            Path(file_path)
        )

        source_code = (
            file_path_obj.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        )

        chunks = []

        # Classes
        for class_info in (
            parsed["classes"]
        ):

            chunks.append(
                CodeChunk(
                    chunk_type="class",
                    name=class_info[
                        "name"
                    ],
                    content=source_code,
                    file_path=file_path,
                    language="Python",
                    imports=parsed[
                        "imports"
                    ]
                )
            )

            # Methods
            for method in (
                class_info["methods"]
            ):

                chunks.append(
                    CodeChunk(
                        chunk_type="method",
                        name=f"{class_info['name']}.{method['name']}",
                        content=source_code,
                        file_path=file_path,
                        language="Python",
                        imports=parsed["imports"],
                        parent_class=class_info["name"],
                        calls=method.get(
                            "calls",
                            []
                        )
                    )
                )

        # Standalone Functions
        for function in (
            parsed["functions"]
        ):

            chunks.append(
                CodeChunk(
                    chunk_type="function",
                    name=function[
                        "name"
                    ],
                    content=source_code,
                    file_path=file_path,
                    language="Python",
                    imports=parsed[
                        "imports"
                    ]
                )
            )

        return chunks