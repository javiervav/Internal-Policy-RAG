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

    async def embed(self, texts: list[str]) -> list[list[float]]:
        response = await self._client.embeddings.create(input=texts, model=self._model)
        return [item.embedding for item in response.data]
