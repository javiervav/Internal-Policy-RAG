import logging
from app.domain.models.text_embedding import TextEmbedding
from app.domain.repositories.document_repository import DocumentRepository
from app.domain.services.text_chunker import TextChunker
from app.domain.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class LoadInitialDataUseCase:

    def __init__(
        self, 
        document_repository: DocumentRepository,
        text_chunker: TextChunker, 
        embedding_service: EmbeddingService
    ):
        self.document_repository = document_repository
        self.text_chunker = text_chunker
        self.embedding_service = embedding_service

    async def execute(self):
        document = await self.document_repository.load_document()
        chunks = self.text_chunker.chunk(document)
        logger.info(f"Document split into {len(chunks)} chunks.")
        embeddings = await self.embedding_service.embed(chunks)
        text_embeddings = [TextEmbedding(text=chunk, embedding=emb) for chunk, emb in zip(chunks, embeddings)]
        logger.info(f"Generated {len(text_embeddings)} embeddings.")
