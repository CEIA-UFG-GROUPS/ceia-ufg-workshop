# Getting Started

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Docker | 24+ |
| Docker Compose | v2 (bundled with Docker Desktop) |
| OpenAI API key | — |

## 1. Clone and configure

```bash
git clone <repo-url> api-autoreg
cd api-autoreg
```

Create a `.env` file in the project root with your OpenAI key:

```bash
OPENAI_API_KEY=sk-...
```

## 2. Start all services

```bash
docker compose up --build -d
```

This brings up four containers:

| Container | Role |
|-----------|------|
| `phoenix` | Arize Phoenix tracing UI |
| `api` | FastAPI backend |
| `streamlit` | Browser UI |
| `mkdocs` | This documentation site |

Wait for the API health check to pass (about 10–15 seconds):

```bash
docker compose ps
```

## 3. Open the services

- **Streamlit UI** → [http://localhost:8501](http://localhost:8501)
- **Swagger / ReDoc** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **Phoenix tracing** → [http://localhost:6006](http://localhost:6006)
- **Docs** → [http://localhost:8080](http://localhost:8080)

## 4. Default credentials

The default credentials are configured via `APP_USER` in `docker-compose.yml`:

| Field | Default value |
|-------|---------------|
| Username | `admin` |
| Password | `changeme` |

> **Change these before deploying to any shared environment.**
> Set `APP_USER=youruser:strongpassword` and `SECRET_KEY=<random-64-char-string>` in your environment or `.env`.

## 5. Quick test with cURL

```bash
# 1. Obtain a token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=changeme" | jq -r .access_token)

# 2. Upload a document
curl -s -X POST http://localhost:8000/documents \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@/path/to/document.pdf"

# 3. Ask a question
curl -s -X POST http://localhost:8000/rag/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```
