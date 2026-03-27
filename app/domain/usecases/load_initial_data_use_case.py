class LoadInitialDataUseCase:
    def __init__(self, document_repository, text_chunker):
        self.document_repository = document_repository
        self.text_chunker = text_chunker

    async def execute(self) -> list[str]:
        document = self.document_repository.load_document()
        chunks = self.text_chunker.chunk(document)
        print(f"Document split into {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            print(f"\n--- Chunk {i + 1} ---\n{chunk}")
        return chunks
