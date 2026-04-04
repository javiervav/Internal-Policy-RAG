import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.models.text_embedding import TextEmbedding
from app.domain.usecases.load_initial_data_use_case import LoadInitialDataUseCase


@pytest.fixture
def document_repository():
    mock = AsyncMock()
    mock.load_document.return_value = "Title\n1. First section\nContent A"
    return mock

@pytest.fixture
def text_chunker():
    mock = MagicMock()
    mock.chunk.return_value = ["Title", "1. First section\nContent A"]
    return mock

@pytest.fixture
def embedding_service():
    mock = AsyncMock()
    mock.embed_texts.return_value = [[0.1, 0.2], [0.3, 0.4]]
    return mock

@pytest.fixture
def vector_store_repository():
    mock = AsyncMock()
    mock.is_empty.return_value = True
    return mock

@pytest.fixture
def use_case(document_repository, text_chunker, embedding_service, vector_store_repository):
    return LoadInitialDataUseCase(
        document_repository=document_repository,
        vector_store_repository=vector_store_repository,
        text_chunker=text_chunker,
        embedding_service=embedding_service,
    )


async def test_execute_loads_chunks_and_stores_embeddings(use_case, document_repository, text_chunker, embedding_service, vector_store_repository):
    await use_case.execute()

    document_repository.load_document.assert_called_once()
    text_chunker.chunk.assert_called_once_with("Title\n1. First section\nContent A")
    embedding_service.embed_texts.assert_called_once_with(["Title", "1. First section\nContent A"])
    vector_store_repository.add.assert_called_once_with([
        TextEmbedding(text="Title", embedding=[0.1, 0.2]),
        TextEmbedding(text="1. First section\nContent A", embedding=[0.3, 0.4]),
    ])


async def test_execute_skips_loading_when_store_is_not_empty(use_case, document_repository, vector_store_repository):
    vector_store_repository.is_empty.return_value = False

    await use_case.execute()

    document_repository.load_document.assert_not_called()
    vector_store_repository.add.assert_not_called()