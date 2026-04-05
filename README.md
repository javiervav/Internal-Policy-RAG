# Internal Policy RAG

This project uses a Retrieval-Augmented Generation (RAG) approach to query and extract information from TechSolutions S.L.'s internal policy document.

## Description

The goal is to enable automated queries on the company's internal manual, leveraging natural language processing and information retrieval techniques.

On startup, the application loads and indexes the policy documents. Users can then ask natural-language questions via a REST API and receive answers grounded in the document content.

## Screenshot

![UI Screenshot](https://github.com/user-attachments/assets/35197c68-a24a-483a-b27a-9a3c4fab9bee)

## Architecture

The project follows **Clean Architecture**.

```
app/
├── api/             # Entry point
├── domain/          # Core business
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── usecases/
├── data/            # Repository & datasource implementations
│   ├── datasources/
│   └── repositories/
├── infrastructure/  # External service implementations
└── di/              # Dependency injection container
```

### Domain layer (`app/domain/`)

The heart of the application. Contains no external dependencies — only pure Python and abstract interfaces.

- **Models** — Core data structures (e.g. `TextEmbedding`).
- **Repository interfaces** — Abstract contracts for data access (`DocumentRepository`, `VectorStoreRepository`). The domain defines *what* it needs, not *how* it is implemented.
- **Service interfaces** — Abstract contracts for external capabilities (`EmbeddingService`, `LLMService`, `TextChunker`).
- **Use cases** — Orchestrate the business logic:
  - `LoadInitialDataUseCase` — Reads source documents, splits them into chunks, generates embeddings, and stores them in the vector store.
  - `AskQuestionUseCase` — Embeds the user's question, retrieves the most similar document chunks from the vector store, and sends them as context to the LLM to produce a grounded answer.

### Data layer (`app/data/`)

Implements the repository interfaces defined in the domain.

- **Datasources** — Low-level I/O abstractions:
  - `DocumentLocalFileDatasource` — Reads PDF documents from the local filesystem.
  - `ChromaVectorStore` — Persists embeddings and documents to disk using [Chroma](https://www.trychroma.com/), with cosine similarity as the distance metric. The store survives server restarts, so documents are only indexed once.
  - `InMemoryVectorStore` — Alternative in-memory implementation using NumPy cosine similarity. Useful for testing or lightweight setups where persistence is not needed.
- **Repositories** — Implement the domain repository interfaces by composing one or more datasources (`DocumentRepositoryImpl`, `VectorStoreRepositoryImpl`).

### Infrastructure layer (`app/infrastructure/`)

Implements the service interfaces defined in the domain using third-party libraries and external APIs.

- `OpenAIEmbeddingService` — Calls the OpenAI Embeddings API (`text-embedding-3-small`) to convert text into vector representations.
- `OpenAILLMService` — Calls the OpenAI Chat Completions API to generate answers given a question and retrieved context.
- `ManualTextChunker` — Splits raw document text into smaller chunks suitable for embedding and retrieval.

### API layer (`app/api/`)

The outermost layer. Exposes the application over HTTP using **FastAPI**.

- On startup, triggers `LoadInitialDataUseCase` to index the documents.
- `POST /ask?question=...` — Delegates to `AskQuestionUseCase` and returns the answer.

### Dependency injection (`app/di/`)

The `Container` class wires together all concrete implementations and injects them into use cases. This is the only place in the codebase where concrete classes are instantiated and assembled, keeping every other layer decoupled.

## Tech stack

| Concern | Library |
| --- | --- |
| REST API | FastAPI + Uvicorn |
| LLM & Embeddings | OpenAI API |
| PDF parsing | pypdf |
| Vector store | Chroma (persistent, cosine similarity) |
| Vector similarity | NumPy (in-memory) |
| Testing | pytest + pytest-asyncio |

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

3. Run the server:
   ```bash
   fastapi dev app/api/main.py
   ```

4. Open `http://localhost:8000` in your browser and ask a question. Some examples:
   - Can I use software for personal purposes?
   - How many vacation days do I have?

## Running tests

```bash
pytest
```
