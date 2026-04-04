import asyncio
import uuid
import chromadb
from app.data.datasources.vector_store_datasource import VectorStoreDatasource
from app.domain.models.text_embedding import TextEmbedding

COLLECTION_NAME = "documents"


class ChromaVectorStore(VectorStoreDatasource):

    def __init__(self, path: str = "./chroma_db"):
        client = chromadb.PersistentClient(path=path)
        self._collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            configuration={"hnsw": {"space": "cosine"}},
        )

    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        await asyncio.to_thread(self._add, text_embeddings)

    async def is_empty(self) -> bool:
        return await asyncio.to_thread(lambda: self._collection.count() == 0)

    async def search_similarities(
            self,
            embedded_question: list[float],
            max_results: int,
            threshold: float,
    ) -> list[str]:
        return await asyncio.to_thread(self._search, embedded_question, max_results, threshold)

    def _add(self, text_embeddings: list[TextEmbedding]) -> None:
        self._collection.add(
            ids=[str(uuid.uuid4()) for _ in text_embeddings],
            embeddings=[te.embedding for te in text_embeddings],
            documents=[te.text for te in text_embeddings],
        )

    def _search(self, embedded_question: list[float], max_results: int, threshold: float) -> list[str]:
        results = self._collection.query(
            query_embeddings=[embedded_question],
            n_results=max_results,
        )
        documents = results["documents"][0]
        distances = results["distances"][0]
        return [doc for doc, distance in zip(documents, distances) if (1 - distance) >= threshold]
