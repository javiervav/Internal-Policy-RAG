import logging

from app.domain.repositories.vector_store_repository import VectorStoreRepository
from app.domain.services.embedding_service import EmbeddingService
from app.domain.services.llm_service import LLMService

logger = logging.getLogger(__name__)

MAX_RESULTS = 3
SIMILARITY_THRESHOLD = 0.3
MAX_OUTPUT_TOKENS = 300


class AskQuestionUseCase:

    def __init__(
            self,
            embedding_service: EmbeddingService,
            vector_store_repository: VectorStoreRepository,
            llm_service: LLMService,
    ):
        self._embedding_service = embedding_service
        self._vector_store_repository = vector_store_repository
        self._llm_service = llm_service

    async def execute(self, question) -> str:
        embedded_question = await self._embedding_service.embed_text(question)
        relevant_documents = await self._vector_store_repository.get_relevant_documents(
            embedded_question=embedded_question,
            max_results=MAX_RESULTS,
            threshold=SIMILARITY_THRESHOLD
        )
        context = "\n\n".join(relevant_documents)
        logger.info(f"Getting answer for question: {question}\nContext: {context}")
        answer = await self._llm_service.get_answer(
            question=question,
            context=context,
            max_output_tokens=MAX_OUTPUT_TOKENS
        )
        logger.info(f"Answer: {answer}")
        return answer
