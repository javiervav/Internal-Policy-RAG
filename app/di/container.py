from openai import AsyncOpenAI
from app.data.datasources.document_local_file_datasource import DocumentLocalFileDatasource
from app.data.datasources.in_memory_vector_store import InMemoryVectorStore
from app.data.repositories.vector_store_repository_impl import VectorStoreRepositoryImpl
from app.data.repositories.document_repository_impl import DocumentRepositoryImpl
from app.data.services.openai_embedding_service import OpenAIEmbeddingService
from app.domain.services.text_chunker import TextChunker
from app.domain.usecases.load_initial_data_use_case import LoadInitialDataUseCase

class Container:

    def __init__(self):
        document_datasource = DocumentLocalFileDatasource()
        document_repository = DocumentRepositoryImpl(document_datasource)
        
        text_chunker = TextChunker()
        
        embedding_service = OpenAIEmbeddingService(client=AsyncOpenAI())
        
        vector_store_datasource = InMemoryVectorStore()
        vector_store_repository = VectorStoreRepositoryImpl(vector_store_datasource)
        
        self.load_initial_data_use_case = LoadInitialDataUseCase(
            document_repository=document_repository,
            vector_store_repository=vector_store_repository,
            text_chunker=text_chunker,
            embedding_service=embedding_service
        )
