from pathlib import Path
import asyncio
from pypdf import PdfReader
from app.data.datasources.document_datasource import DocumentDatasource

DOCUMENT_PATH = Path(__file__).parents[2] / "ingestion" / "Internal Policy.pdf"

class DocumentLocalFileDatasource(DocumentDatasource):
    def __init__(self, path: str = DOCUMENT_PATH):
        self.path = path

    async def load(self) -> str:
        return await asyncio.to_thread(self._read_pdf)

    def _read_pdf(self) -> str:
        reader = PdfReader(self.path)
        pages = [page.extract_text() for page in reader.pages]
        return "\n".join(pages)
