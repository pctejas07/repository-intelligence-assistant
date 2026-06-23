import ollama

from app.core.config import settings


class LLMService:

    @staticmethod
    def generate_answer(
        query: str,
        contexts: list[str]
    ) -> str:

        context_text = "\n\n".join(
            contexts
        )

        prompt = f"""
            You are a senior software engineer.

            Use BOTH:

            1. Repository code context
            2. Graph relationships between classes, methods, inheritance, imports and dependencies

            to answer the question.

            Repository Context:

            {context_text}

            Question:

            {query}

            Provide:

            1. Direct Answer
            2. Architecture Explanation
            3. Relevant Classes/Methods
            4. Related Dependencies (if available)

            Do not invent files, classes, methods or dependencies that are not present in the provided context.
            """
        from app.core.logger import logger

        logger.info(
            f"Context chars: {len(context_text)}"
        )

        logger.info(
            f"Prompt chars: {len(prompt)}"
        )


        logger.info(
            f"Using model: {settings.LLM_MODEL}"
        )
        
        response = ollama.chat(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            think=False
        )

        return response["message"]["content"]