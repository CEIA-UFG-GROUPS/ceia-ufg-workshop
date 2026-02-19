# API Reference

The full interactive spec is also available at **[http://localhost:8000/docs](http://localhost:8000/docs)** (Swagger UI) and **[http://localhost:8000/redoc](http://localhost:8000/redoc)** (ReDoc).

---

## Authentication

All endpoints except `/health` and `/auth/login` require a `Bearer` token in the `Authorization` header.

---

## Endpoints

### `GET /health`

Returns the service health status. Used by Docker health checks and load balancers.

**Auth:** None

**Response `200`**

```json
{ "status": "ok" }
```

**cURL**

```bash
curl http://localhost:8000/health
```

---

### `POST /auth/login`

Obtain a JWT access token using username and password.

**Auth:** None

**Request** — `application/x-www-form-urlencoded`

| Field | Type | Description |
|-------|------|-------------|
| `username` | string | Configured user (default: `admin`) |
| `password` | string | Configured password (default: `changeme`) |

**Response `200`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

| Field | Description |
|-------|-------------|
| `access_token` | JWT string to use in subsequent requests |
| `token_type` | Always `"bearer"` |
| `expires_in` | Seconds until expiry (default: 1800 = 30 min) |

**Response `401`** — Invalid credentials

**cURL**

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=changeme"
```

---

### `POST /documents`

Upload one or more documents. PDF and TXT files are saved and indexed for RAG. Other file types are saved but not indexed.

**Auth:** Bearer token required

**Request** — `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `files` | file[] | One or more files to upload |

**Response `200`**

```json
{ "documents": ["report.pdf", "notes.txt"] }
```

**Response `401`** — Missing or invalid token
**Response `422`** — Validation error (no files provided)

**cURL**

```bash
TOKEN="<your-token>"

# Single file
curl -X POST http://localhost:8000/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@report.pdf"

# Multiple files
curl -X POST http://localhost:8000/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@report.pdf" \
  -F "files=@notes.txt"
```

---

### `POST /rag/query`

Ask a natural-language question. The API retrieves the most relevant chunks from the FAISS index and uses GPT-4o-mini to synthesize an answer.

**Auth:** Bearer token required

**Request** — `application/json`

```json
{ "question": "What are the main conclusions of the audit report?" }
```

**Response `200`**

```json
{
  "answer": "The audit report concludes that...",
  "sources": ["/app/uploads/report.pdf", "/app/uploads/notes.txt"]
}
```

| Field | Description |
|-------|-------------|
| `answer` | LLM-generated answer based on retrieved context |
| `sources` | List of source file paths whose chunks were used |

**Response `401`** — Missing or invalid token
**Response `404`** — No documents have been indexed yet

**cURL**

```bash
TOKEN="<your-token>"

curl -X POST http://localhost:8000/rag/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the key findings."}'
```

---

### `GET /rag/documents`

List the unique document filenames currently stored in the FAISS index.

**Auth:** Bearer token required

**Response `200`**

```json
{ "documents": ["notes.txt", "report.pdf"] }
```

**Response `401`** — Missing or invalid token

**cURL**

```bash
TOKEN="<your-token>"

curl http://localhost:8000/rag/documents \
  -H "Authorization: Bearer $TOKEN"
```
