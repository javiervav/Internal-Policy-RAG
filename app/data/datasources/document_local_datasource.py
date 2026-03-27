from pypdf import PdfReader


class DocumentLocalDatasource:

    def load(self) -> str:
        reader = PdfReader("app/ingestion/Internal Policy.pdf")
        pages = [page.extract_text() for page in reader.pages]
        return "\n".join(pages)
