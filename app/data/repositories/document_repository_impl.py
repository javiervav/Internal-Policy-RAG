from app.data.datasources.document_datasource import DocumentDatasource
from app.domain.repositories.document_repository import DocumentRepository

class DocumentRepositoryImpl(DocumentRepository):
    def __init__(self, document_datasource: DocumentDatasource):
        self.document_datasource = document_datasource

    async def load_document(self) -> str:
        return await self.document_datasource.load()
