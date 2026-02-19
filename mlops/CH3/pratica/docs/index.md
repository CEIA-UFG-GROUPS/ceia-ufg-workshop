# API AutoReg

**API AutoReg** is a Document Q&A service built for SEFAZ. Upload PDF and TXT documents and query them through a Retrieval-Augmented Generation (RAG) pipeline powered by LangChain and OpenAI.

## Features

- **Document ingestion** — Upload multiple PDF or TXT files in a single request.
- **RAG querying** — Ask natural-language questions; the API retrieves relevant chunks and synthesizes an answer using GPT-4o-mini.
- **JWT authentication** — All document and query endpoints require a Bearer token obtained via `/auth/login`.
- **Streamlit UI** — A browser-based chat interface for non-technical users.
- **Observability** — Distributed tracing with Arize Phoenix (OpenTelemetry).
- **Containerized** — The entire stack runs with a single `docker compose up`.

## Service Ports

| Service | Port | URL |
|---------|------|-----|
| FastAPI backend | 8000 | `http://localhost:8000` |
| Interactive API docs (Swagger) | 8000 | `http://localhost:8000/docs` |
| Streamlit UI | 8501 | `http://localhost:8501` |
| Arize Phoenix (tracing) | 6006 | `http://localhost:6006` |
| MkDocs (this site) | 8080 | `http://localhost:8080` |
