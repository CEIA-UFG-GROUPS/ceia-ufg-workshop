# RAG Pipeline

API AutoReg implements a Retrieval-Augmented Generation (RAG) pipeline using LangChain. Documents are ingested once on upload and queried on demand.

## Supported File Formats

| Extension | Loader | Notes |
|-----------|--------|-------|
| `.pdf` | `PyPDFLoader` | Extracts text from each page |
| `.txt` | `TextLoader` | UTF-8 encoding assumed |

Other file types (e.g. `.docx`, `.xlsx`) are accepted by the upload endpoint and saved to disk, but **not** indexed for RAG.

---

## Ingestion Flow

```
Uploaded file
    │
    ▼
Load document
  ├── .pdf  → PyPDFLoader  (one Document per page)
  └── .txt  → TextLoader   (one Document for the whole file)
    │
    ▼
RecursiveCharacterTextSplitter
  chunk_size   = 1 000 characters
  chunk_overlap = 150 characters
    │
    ▼
OpenAIEmbeddings
  model: text-embedding-ada-002
    │
    ▼
FAISS vector store (persisted to VECTORSTORE_DIR)
  ├── First upload  → FAISS.from_documents(chunks, embeddings)
  └── Subsequent   → FAISS.load_local() + vs.add_documents(chunks)
```

> Ingestion is protected by an `asyncio.Lock` so concurrent uploads do not corrupt the index.

---

## Query Flow

```
POST /rag/query { "question": "..." }
    │
    ▼
Load FAISS index from VECTORSTORE_DIR
    │
    ▼
Retriever: similarity search, k=4
  → returns top-4 most relevant chunks
    │
    ├── Collect source paths for the response
    │
    ▼
LangChain LCEL chain:
  {"context": retriever | format_docs, "question": passthrough}
    │
    ▼
ChatPromptTemplate
  "Answer the question based on the following context:
   {context}

   Question: {question}"
    │
    ▼
ChatOpenAI
  model: gpt-4o-mini (configurable via OPENAI_MODEL)
  temperature: 0
    │
    ▼
StrOutputParser
    │
    ▼
Response { "answer": "...", "sources": [...] }
```

---

## Storage

| Path (container) | Content |
|------------------|---------|
| `/app/uploads/` | Raw uploaded files |
| `/app/vectorstore/index.faiss` | FAISS binary index |
| `/app/vectorstore/index.pkl` | FAISS docstore (metadata) |

Both directories are backed by the `rag_data` Docker volume, so the index persists across container restarts.

---

## Limitations

- The FAISS index is **not deduplicated**: uploading the same file twice adds its chunks twice.
- Only one FAISS index exists globally; there is no per-user or per-collection separation.
- Large PDFs with many pages may increase ingestion time significantly because each page triggers an embedding API call batch.
