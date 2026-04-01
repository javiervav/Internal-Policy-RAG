import logging

from app.domain.repositories.vector_store_repository import VectorStoreRepository
from app.domain.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

MAX_RESULTS = 3
SIMILARITY_THRESHOLD = 0.3


class AskQuestionUseCase:

    def __init__(
            self,
            embedding_service: EmbeddingService,
            vector_store_repository: VectorStoreRepository,
    ):
        self._embedding_service = embedding_service
        self._vector_store_repository = vector_store_repository

    async def execute(self, question):
        embedded_question = await self._embedding_service.embed_text(question)
        relevant_documents = await self._vector_store_repository.get_relevant_documents(
            embedded_question=embedded_question,
            max_results=MAX_RESULTS,
            threshold=SIMILARITY_THRESHOLD
        )
        context = "\n\n".join(relevant_documents)

    # # 1. Generar embedding de la pregunta
    # embedding = get_embedding(question)
    #
    # # 2. Recuperar los documentos más relevantes
    # results = vectorStore.search(
    #     query_embedding=embedding,
    #     top_k=3,
    #     threshold=0.3
    # )
    #
    # # 3. Combinar los documentos en un bloque de texto
    # context = "\n\n".join(results)
    #
    # # 4. Llamar al LLM para generar la respuesta usando el contexto
    # answer = get_answer(question, context)
    #
    # return {
    #     "question": question,
    #     "answer": answer,
    #     "results": results
    # }
