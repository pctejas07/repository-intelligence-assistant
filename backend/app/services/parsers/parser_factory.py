from app.services.parsers.python_parser import (
    PythonParser
)

from app.services.parsers.java_parser import (
    JavaParser
)


class ParserFactory:

    @staticmethod
    def get_parser(
        language: str
    ):

        if language == "Python":

            return PythonParser

        if language == "Java":

            return JavaParser

        return None