from openai import AsyncOpenAI
from app.data.datasources.document_local_file_datasource import DocumentLocalFileDatasource
from app.data.datasources.in_memory_vector_store import InMemoryVectorStore
from app.data.repositories.vector_store_repository_impl import VectorStoreRepositoryImpl
from app.data.repositories.document_repository_impl import DocumentRepositoryImpl
from app.infrastructure.openai_embedding_service import OpenAIEmbeddingService
from app.infrastructure.manual_text_chunker import ManualTextChunker
from app.domain.usecases.ask_question_use_case import AskQuestionUseCase
from app.domain.usecases.load_initial_data_use_case import LoadInitialDataUseCase


class Container:

    def __init__(self):
        document_datasource = DocumentLocalFileDatasource()
        document_repository = DocumentRepositoryImpl(document_datasource)

        text_chunker = ManualTextChunker()

        embedding_service = OpenAIEmbeddingService(client=AsyncOpenAI())

        vector_store_datasource = InMemoryVectorStore()
        vector_store_repository = VectorStoreRepositoryImpl(vector_store_datasource)

        self.load_initial_data_use_case = LoadInitialDataUseCase(
            document_repository=document_repository,
            vector_store_repository=vector_store_repository,
            text_chunker=text_chunker,
            embedding_service=embedding_service
        )

        self.ask_question_use_case = AskQuestionUseCase(
            embedding_service=embedding_service,
            vector_store_repository=vector_store_repository,
        )
