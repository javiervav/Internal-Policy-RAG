from contextlib import asynccontextmanager
from app.data.datasources.document_local_datasource import DocumentLocalDatasource
from app.data.repositories.document_repository import DocumentRepository
from app.domain.services.text_chunker import TextChunker
from app.domain.usecases.load_initial_data_use_case import LoadInitialDataUseCase
from fastapi import FastAPI

datasource = DocumentLocalDatasource()
document_repository = DocumentRepository(datasource)
text_chunker = TextChunker()
load_initial_data_use_case = LoadInitialDataUseCase(document_repository, text_chunker)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading initial data...")
    await load_initial_data_use_case.execute()
    print("Initial data loaded.")
    yield


app = FastAPI(lifespan=lifespan)