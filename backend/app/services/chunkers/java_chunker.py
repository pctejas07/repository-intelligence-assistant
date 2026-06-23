from pathlib import Path

from app.models.chunk import (
    CodeChunk
)

from app.services.parsers.java_parser import (
    JavaParser
)


class JavaChunker:

    @staticmethod
    def chunk(
        file_path: str
    ):

        parsed = (
            JavaParser.parse(
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

        for class_info in (
            parsed["classes"]
        ):

            chunks.append(
                CodeChunk(
                    chunk_type=class_info.get(
                        "type",
                        "class"
                    ),
                    name=class_info[
                        "name"
                    ],
                    content=source_code,
                    file_path=file_path,
                    language="Java",
                    package_name=parsed[
                        "package"
                    ],
                    imports=parsed[
                        "imports"
                    ],
                    extends=class_info[
                        "extends"
                    ],
                    implements=class_info[
                        "implements"
                    ]
                )
            )

            for method in (
                class_info["methods"]
            ):
                

                chunks.append(
                    CodeChunk(
                        chunk_type="method",
                        name=f"{class_info['name']}.{method['name']}",
                        content=source_code,
                        file_path=file_path,
                        language="Java",
                        package_name=parsed[
                            "package"
                        ],
                        imports=parsed[
                            "imports"
                        ],
                        parent_class=class_info[
                            "name"
                        ],
                        extends=class_info[
                            "extends"
                        ],
                        implements=class_info[
                            "implements"
                        ],
                        calls=method.get(
                            "calls",
                            []
                        )
                    )
                )

        return chunks