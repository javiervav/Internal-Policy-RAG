from app.data.datasources.document_datasource import DocumentDatasource
from app.domain.repositories.document_repository import DocumentRepository

class DocumentRepositoryImpl(DocumentRepository):
    def __init__(self, document_datasource: DocumentDatasource):
        self.document_datasource = document_datasource

    def load_document(self) -> str:
        return self.document_datasource.load()
