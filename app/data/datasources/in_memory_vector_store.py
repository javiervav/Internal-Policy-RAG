import asyncio
import numpy
from app.data.datasources.vector_store_datasource import VectorStoreDatasource
from app.domain.models.text_embedding import TextEmbedding


class InMemoryVectorStore(VectorStoreDatasource):

    def __init__(self):
        self.texts: list[str] = []
        self.vectors: list[list[float]] = []

    async def add(self, text_embeddings: list[TextEmbedding]) -> None:
        await asyncio.to_thread(self._add_embeddings, text_embeddings)

    async def is_empty(self) -> bool:
        return len(self.vectors) == 0

    async def search_similarities(
            self,
            embedded_question: list[float],
            max_results: int,
            threshold: float,
    ) -> list[str]:
        similarities: list[float] = self._get_vector_similarities(embedded_question)
        top_indexes: list[int] = self._get_top_similarity_indexes(similarities, max_results)
        most_similar_texts = self._filter_texts_by_threshold(top_indexes, similarities, threshold)
        return most_similar_texts

    def _add_embeddings(self, text_embeddings: list[TextEmbedding]) -> None:
        for te in text_embeddings:
            self.texts.append(te.text)
            self.vectors.append(te.embedding)

    # Compares the embedded question against every stored vector and returns a similarity score for each.
    def _get_vector_similarities(self, embedded_question: list[float]) -> list[float]:
        similarities = []
        for vector in self.vectors:
            similarity = self._cosine_similarity(embedded_question, vector)
            similarities.append(similarity)
        return similarities

    @staticmethod
    # Measures the angle between two vectors. Returns 1 if identical, 0 if orthogonal, -1 if opposite.
    def _cosine_similarity(vector1: list[float], vector2: list[float]) -> float:
        array1, array2 = numpy.array(vector1), numpy.array(vector2)
        return numpy.dot(array1, array2) / (numpy.linalg.norm(array1) * numpy.linalg.norm(array2))

    @staticmethod
    def _get_top_similarity_indexes(similarities: list[float], max_results: int) -> list[int]:
        return numpy.argsort(similarities)[-max_results:][::-1].tolist()

    # Returns only the texts whose similarity score meets or exceeds the threshold.
    def _filter_texts_by_threshold(self, indices: list[int], similarities: list[float], threshold: float) -> list[str]:
        return [self.texts[i] for i in indices if similarities[i] >= threshold]
