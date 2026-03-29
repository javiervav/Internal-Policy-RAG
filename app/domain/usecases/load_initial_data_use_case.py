import logging
from app.domain.repositories.document_repository import DocumentRepository
from app.domain.services.text_chunker import TextChunker

logger = logging.getLogger(__name__)

class LoadInitialDataUseCase:
    def __init__(self, document_repository: DocumentRepository, text_chunker: TextChunker):
        self.document_repository = document_repository
        self.text_chunker = text_chunker

    async def execute(self) -> list[str]:
        document = self.document_repository.load_document()
        chunks = self.text_chunker.chunk(document)
        logger.info(f"Document split into {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            logger.debug(f"\n--- Chunk {i + 1} ---\n{chunk}")
        return chunks
