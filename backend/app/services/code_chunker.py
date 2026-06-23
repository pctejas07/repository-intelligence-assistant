from app.services.chunkers.python_chunker import (
    PythonChunker
)

from app.services.chunkers.java_chunker import (
    JavaChunker
)


class CodeChunker:

    @staticmethod
    def chunk_file(
        file_path: str,
        language: str
    ):

        if language == "Python":

            return (
                PythonChunker.chunk(
                    file_path
                )
            )

        if language == "Java":

            return (
                JavaChunker.chunk(
                    file_path
                )
            )

        return []