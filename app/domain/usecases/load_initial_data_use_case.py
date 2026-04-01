import logging
from app.domain.models.text_embedding import TextEmbedding
from app.domain.repositories.document_repository import DocumentRepository
from app.domain.services.text_chunker import TextChunker
from app.domain.services.embedding_service import EmbeddingService
from app.domain.repositories.vector_store_repository import VectorStoreRepository

logger = logging.getLogger(__name__)


class LoadInitialDataUseCase:

    def __init__(
            self,
            document_repository: DocumentRepository,
            vector_store_repository: VectorStoreRepository,
            text_chunker: TextChunker,
            embedding_service: EmbeddingService,
    ):
        self._document_repository = document_repository
        self._text_chunker = text_chunker
        self._embedding_service = embedding_service
        self._vector_store_repository = vector_store_repository

    async def execute(self):
        document = await self._document_repository.load_document()

        chunks = self._text_chunker.chunk(document)
        logger.info(f"Document split into {len(chunks)} chunks.")

        embeddings = await self._embedding_service.embed_texts(chunks)
        text_embeddings = self._get_text_embeddings(chunks, embeddings)
        logger.info(f"Generated {len(text_embeddings)} embeddings.")

        await self._vector_store_repository.add(text_embeddings)
        logger.info(f"Stored {len(text_embeddings)} embeddings in vector store.")

    @staticmethod
    def _get_text_embeddings(chunks: list[str], embeddings: list[list[float]]) -> list[TextEmbedding]:
        return [TextEmbedding(text=chunk, embedding=emb) for chunk, emb in zip(chunks, embeddings)]
