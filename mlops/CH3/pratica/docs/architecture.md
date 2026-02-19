# Architecture

## Service Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        docker network                           │
│                                                                 │
│  ┌──────────────┐     ┌──────────────────────────────────────┐  │
│  │  Streamlit   │────▶│           FastAPI (api)              │  │
│  │  :8501       │     │           :8000                      │  │
│  └──────────────┘     │  ┌────────────┐  ┌────────────────┐  │  │
│                        │  │  Auth (JWT)│  │ RAG endpoints  │  │  │
│  ┌──────────────┐     │  └────────────┘  └───────┬────────┘  │  │
│  │  MkDocs      │     └──────────────────────────┼───────────┘  │
│  │  :8080       │                                │              │
│  └──────────────┘     ┌──────────────────────────▼───────────┐  │
│                        │        LangChain RAG pipeline        │  │
│                        │  PyPDF / TextLoader → Splitter →    │  │
│                        │  OpenAIEmbeddings → FAISS index      │  │
│                        └──────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────┐                                               │
│  │  Phoenix     │◀── OpenTelemetry traces from FastAPI          │
│  │  :6006       │                                               │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘

   Volumes:
     phoenix_data  →  /mnt/data  (Phoenix traces)
     rag_data      →  /app/uploads + /app/vectorstore (FAISS index)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API framework | FastAPI + Uvicorn |
| Authentication | OAuth2 Password Flow + JWT (python-jose) |
| Password hashing | passlib sha256_crypt |
| Document loading | LangChain `PyPDFLoader`, `TextLoader` |
| Text splitting | `RecursiveCharacterTextSplitter` (1000 chars, 150 overlap) |
| Embeddings | OpenAI `text-embedding-ada-002` (via `langchain-openai`) |
| Vector store | FAISS (persisted to disk) |
| LLM | OpenAI `gpt-4o-mini` |
| UI | Streamlit |
| Tracing | Arize Phoenix + OpenTelemetry |
| Runtime | Python 3.13, uv |
| Containerization | Docker + Docker Compose |
| Docs | MkDocs Material |

## Data Flow

### Upload flow

```
Client
  │
  ├─ POST /auth/login  →  JWT token
  │
  └─ POST /documents (multipart, Bearer token)
       │
       ├─ Save raw file to UPLOAD_DIR (/app/uploads)
       │
       └─ If .pdf or .txt AND OPENAI_API_KEY is set:
            │
            ├─ Load document (PyPDFLoader / TextLoader)
            ├─ Split into chunks (1000 chars, 150 overlap)
            ├─ Embed chunks (OpenAI embeddings)
            └─ Upsert into FAISS index (VECTORSTORE_DIR)
```

### Query flow

```
Client
  │
  └─ POST /rag/query { "question": "..." } (Bearer token)
       │
       ├─ Load FAISS index from disk
       ├─ Retrieve top-4 relevant chunks
       ├─ Build prompt: context + question
       ├─ Call ChatOpenAI (gpt-4o-mini, temperature=0)
       └─ Return { "answer": "...", "sources": [...] }
```
