import pytest
from unittest.mock import AsyncMock
from app.domain.usecases.ask_question_use_case import AskQuestionUseCase


@pytest.fixture
def embedding_service():
    mock = AsyncMock()
    mock.embed_text.return_value = [0.1, 0.2, 0.3]
    return mock


@pytest.fixture
def vector_store_repository():
    mock = AsyncMock()
    mock.get_relevant_documents.return_value = [
        "Employees are provided with a laptop.",
        "Equipment must be returned at end of contract."
    ]
    return mock


@pytest.fixture
def llm_service():
    mock = AsyncMock()
    mock.get_answer.return_value = "Yes, employees are provided with a laptop."
    return mock


@pytest.fixture
def use_case(embedding_service, vector_store_repository, llm_service):
    return AskQuestionUseCase(
        embedding_service=embedding_service,
        vector_store_repository=vector_store_repository,
        llm_service=llm_service,
    )


async def test_execute_returns_answer(use_case, embedding_service, vector_store_repository, llm_service):
    answer = await use_case.execute("Do I have a computer provided by the company?")

    embedding_service.embed_text.assert_called_once_with("Do I have a computer provided by the company?")
    vector_store_repository.get_relevant_documents.assert_called_once_with(
        embedded_question=[0.1, 0.2, 0.3],
        max_results=3,
        threshold=0.3,
    )
    llm_service.get_answer.assert_called_once_with(
        question="Do I have a computer provided by the company?",
        context="Employees are provided with a laptop.\n\nEquipment must be returned at end of contract.",
        max_output_tokens=300,
    )
    assert answer == "Yes, employees are provided with a laptop."
