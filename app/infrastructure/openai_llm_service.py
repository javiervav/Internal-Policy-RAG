from openai import AsyncOpenAI

from app.domain.services.llm_service import LLMService


class OpenAILLMService(LLMService):

    def __init__(
            self,
            client: AsyncOpenAI,
            model: str,
    ) -> None:
        self._open_ai_client = client
        self._model = model

    async def get_answer(
            self,
            question: str,
            context: str,
            max_output_tokens: int
    ) -> str:
        prompt = self._get_prompt_template(question, context)
        response = await self._open_ai_client.responses.create(
            model=self._model,
            input=prompt,
            max_output_tokens=max_output_tokens,
        )
        return response.output_text

    @staticmethod
    def _get_prompt_template(question: str, context: str) -> str:
        return f"""
            You are a QA system that answers ONLY using the provided context.
            
            Rules:
            - If the answer is not explicitly in the context, respond EXACTLY with: I don't know
            - Do NOT infer, guess, or use prior knowledge
            - Do NOT return an empty answer
            
            Context:
            {context}
            
            Question:
            {question}
            
            Answer:
            """
