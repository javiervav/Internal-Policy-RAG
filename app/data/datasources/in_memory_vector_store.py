import asyncio
from app.data.datasources.vector_store_datasource import VectorStoreDatasource
from app.domain.models.text_embedding import TextEmbedding

class InMemoryVectorStore(VectorStoreDatasource):
    
    def __init__(self):
        self.texts: list[str] = []
        self.vectors: list[list[float]] = []

    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        await asyncio.to_thread(self._add_embeddings,text_embeddings)

    def _add_embeddings(self, text_embeddings: list[TextEmbedding]) -> None:
        for te in text_embeddings:
            self.texts.append(te.text)
            self.vectors.append(te.embedding)
