from abc import ABC, abstractmethod


class LLMService(ABC):

    @abstractmethod
    async def get_answer(self, question: str, context: str, max_output_tokens: int) -> str:
        pass
