from app.data.datasources.document_local_file_datasource import DocumentLocalFileDatasource
from app.data.repositories.document_repository_impl import DocumentRepositoryImpl
from app.domain.services.text_chunker import TextChunker
from app.domain.usecases.load_initial_data_use_case import LoadInitialDataUseCase


class Container:
    def __init__(self):
        datasource = DocumentLocalFileDatasource()
        repository = DocumentRepositoryImpl(datasource)
        text_chunker = TextChunker()
        self.load_initial_data_use_case = LoadInitialDataUseCase(repository, text_chunker)
