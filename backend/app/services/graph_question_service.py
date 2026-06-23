import re


class GraphQuestionService:

    @staticmethod
    def detect_question_type(
        question: str
    ):

        question = question.lower()

        if (
            "who calls" in question
            or "callers" in question
        ):
            return "callers"

        if (
            "what does" in question
            and "call" in question
        ):
            return "callees"

        if (
            "affected" in question
            or "impact" in question
        ):
            return "impact"

        if (
            "call chain" in question
            or "execution flow" in question
        ):
            return "call_chain"

        if (
            "structure" in question
            or "hierarchy" in question
            or "methods" in question
            or "everything about" in question
        ):
            return "graph_summary"
        
        if (
            "explain" in question
            or "describe" in question
            or "relationships" in question
        ):
            return "method_summary"
        
        return None

    @staticmethod
    def extract_method_name(
        question: str
    ):

        matches = re.findall(
            r"[A-Z][A-Za-z0-9_]*\.[A-Za-z0-9_]+",
            question
        )

        if matches:

            return matches[0]

        return None
    
    @staticmethod
    def extract_class_name(
        question: str
    ):

        import re

        matches = re.findall(
            r"\b[A-Z][A-Za-z0-9_]*\b",
            question
        )

        ignore = {
            "Show",
            "Explain",
            "Describe",
            "What",
            "How",
            "List"
        }

        candidates = [
            m
            for m in matches
            if m not in ignore
        ]

        if candidates:

            return candidates[0]

        return None