import time

from app.services.search_service import SearchService
from app.services.llm_service import LLMService
from app.services.hybrid_search_service import (
    HybridSearchService
)
from app.services.reranker_service import (
    RerankerService
)
from app.core.logger import logger
from app.services.graph_retrieval_service import (
    GraphRetrievalService
)

from app.services.graph_prompt_service import (
    GraphPromptService
)
from app.services.graph_question_service import (
    GraphQuestionService
)
from app.services.graph.call_analysis_service import (
    CallAnalysisService
)
from app.services.graph_answer_service import (
    GraphAnswerService
)
from app.services.graph_summary_service import (
    GraphSummaryService
)

from app.services.graph_summary_prompt_service import (
    GraphSummaryPromptService
)

from app.services.method_summary_service import (
    MethodSummaryService
)

from app.services.method_summary_prompt_service import (
    MethodSummaryPromptService
)

class ChatService:

    @staticmethod
    def ask_repository(
        repository_name: str,
        question: str,
        top_k: int = 5
    ):

        total_start = time.time()

        question_type = (
            GraphQuestionService
            .detect_question_type(
                question
            )
        )

        method_name = (
            GraphQuestionService
            .extract_method_name(
                question
            )
        )

        class_name = (
            GraphQuestionService
            .extract_class_name(
                question
            )
        )

        logger.info(
            f"Class Name: "
            f"{class_name}"
        )

        logger.info(
            f"Question Type: "
            f"{question_type}"
        )

        logger.info(
            f"Method Name: "
            f"{method_name}"
        )

        if (
            question_type
            == "graph_summary"
            and class_name
        ):

            summary = (
                GraphSummaryService
                .summarize_node(
                    repository_name,
                    class_name
                )
            )

            graph_context = (
                GraphSummaryPromptService
                .build_context(
                    summary
                )
            )

            logger.info(
                f"Graph Summary Context:\n"
                f"{graph_context}"
            )

            answer = (
                LLMService.generate_answer(
                    query=question,
                    contexts=[
                        graph_context
                    ]
                )
            )

            return {
                "repository_name":
                repository_name,

                "question":
                question,

                "answer":
                answer,

                "sources": []
            }

        if (
            question_type
            == "method_summary"
            and method_name
        ):

            summary = (
                MethodSummaryService
                .summarize_method(
                    repository_name,
                    method_name
                )
            )

            graph_context = (
                MethodSummaryPromptService
                .build_context(
                    summary
                )
            )

            logger.info(
                f"Method Summary Context:\n"
                f"{graph_context}"
            )

            answer = (
                LLMService.generate_answer(
                    query=question,
                    contexts=[
                        graph_context
                    ]
                )
            )

            return {
                "repository_name":
                repository_name,

                "question":
                question,

                "answer":
                answer,

                "sources": []
            }

        if (
            question_type
            and method_name
        ):

            graph_result = None

            if (
                question_type
                == "callers"
            ):

                graph_result = (
                    CallAnalysisService
                    .get_callers(
                        repository_name,
                        method_name
                    )
                )

            elif (
                question_type
                == "callees"
            ):

                graph_result = (
                    CallAnalysisService
                    .get_callees(
                        repository_name,
                        method_name
                    )
                )

            elif (
                question_type
                == "impact"
            ):

                graph_result = (
                    CallAnalysisService
                    .get_impacted_methods(
                        repository_name,
                        method_name
                    )
                )

            elif (
                question_type
                == "call_chain"
            ):

                graph_result = (
                    CallAnalysisService
                    .get_call_chain(
                        repository_name,
                        method_name
                    )
                )

            logger.info(
                f"Graph Result: "
                f"{graph_result}"
            )

            graph_context = (
                GraphAnswerService
                .build_context(
                    question_type,
                    graph_result
                )
            )

            logger.info(
                f"Graph Context:\n"
                f"{graph_context}"
            )

            answer = (
                LLMService.generate_answer(
                    query=question,
                    contexts=[
                        graph_context
                    ]
                )
            )

            return {
                "repository_name":
                repository_name,

                "question":
                question,

                "answer":
                answer,

                "sources": []
            }

        # Search
        search_start = time.time()

        search_result = (
            HybridSearchService.search(
                repository_name=repository_name,
                query=question,
                top_k=20
            )
        )

        logger.info(
            f"Retrieved: {len(search_result['results'])}"
        )

        logger.info(
            f"Search took "
            f"{time.time() - search_start:.2f}s"
        )

        # Rerank
        rerank_start = time.time()

        reranked_results = (
            RerankerService.rerank(
                query=question,
                results=search_result["results"],
                top_k=top_k
            )
        )
                
        logger.info(
            f"Reranked: {len(reranked_results)}"
        )

        logger.info(
            f"Rerank took "
            f"{time.time() - rerank_start:.2f}s"
        )

        # Graph Expansion

        graph_results = (
            GraphRetrievalService
            .expand_search_results(
                repository_name=repository_name,
                search_results=reranked_results
            )
        )

        logger.info(
            f"Graph expanded results: "
            f"{len(graph_results)}"
        )

        graph_context = (
            GraphPromptService
            .build_context(
                graph_results
            )
        )
        

        logger.info(
            f"Graph context chars: "
            f"{len(graph_context)}"
        )

        contexts = [
            result["content"]
            for result in reranked_results
        ]

        if graph_context:
            contexts.insert(
                0,
                graph_context
            )

        sources = []

        for result in reranked_results:

            sources.append(
                {
                    "file_path": result["file_path"],
                    "chunk_name": result["chunk_name"],
                    "chunk_type": result["chunk_type"]
                }
            )
        
        for i, context in enumerate(contexts):
            logger.info(
                f"Context {i + 1}: {len(context)} chars"
            )


        # LLM
        llm_start = time.time()

        answer = (
            LLMService.generate_answer(
                query=question,
                contexts=contexts
            )
        )

        logger.info(
            f"LLM took "
            f"{time.time() - llm_start:.2f}s"
        )

        logger.info(
            f"Total chat request took "
            f"{time.time() - total_start:.2f}s"
        )

        return {
            "repository_name": repository_name,
            "question": question,
            "answer": answer,
            "sources": sources
        }