from pypdf import PdfReader
from app.data.datasources.document_datasource import DocumentDatasource

DOCUMENT_PATH = "app/ingestion/Internal Policy.pdf"

class DocumentLocalFileDatasource(DocumentDatasource):
    def __init__(self, path: str = DOCUMENT_PATH):
        self.path = path

    def load(self) -> str:
        reader = PdfReader(self.path)
        pages = [page.extract_text() for page in reader.pages]
        return "\n".join(pages)
