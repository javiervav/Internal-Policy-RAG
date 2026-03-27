class DocumentRepository:
    def __init__(self, local_datasource):
        self.local_datasource = local_datasource

    def load_document(self) -> str:
        return self.local_datasource.load()
