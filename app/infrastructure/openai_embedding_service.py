from openai import AsyncOpenAI
from app.domain.services.embedding_service import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):

    def __init__(
            self,
            client: AsyncOpenAI,
            model: str = "text-embedding-3-small"
    ):
        self._client = client
        self._model = model

    async def embed_text(self, text: str) -> list[float]:
        response = await self._client.embeddings.create(input=text, model=self._model)
        return response.data[0].embedding

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = await self._client.embeddings.create(input=texts, model=self._model)
        return [item.embedding for item in response.data]
