# Configuration

All runtime configuration is passed via environment variables. In the Docker Compose stack, most variables are set in `docker-compose.yml` under the `api` service; secrets (like `OPENAI_API_KEY`) are loaded from an `.env` file.

## Environment Variables

### API service (`api`)

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `OPENAI_API_KEY` | — | **Yes** | OpenAI API key. Loaded from `.env`. Without this key, uploaded files are saved to disk but **not** indexed for RAG. |
| `SECRET_KEY` | `CHANGE_ME_IN_PRODUCTION` | **Yes** | Secret used to sign JWT tokens. Use a random 64-character string in production. |
| `APP_USER` | `admin:secret` | No | Single-user credentials in `username:password` format. Change the password before any shared deployment. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | No | JWT lifetime in minutes. |
| `UPLOAD_DIR` | `/tmp/api_autoreg_uploads` | No | Directory where uploaded files are stored inside the container. |
| `VECTORSTORE_DIR` | `/tmp/api_autoreg_vectorstore` | No | Directory where the FAISS index is persisted inside the container. |
| `OPENAI_MODEL` | `gpt-4o-mini` | No | OpenAI chat model used for answer generation. |
| `PHOENIX_COLLECTOR_ENDPOINT` | _(empty)_ | No | OTLP/HTTP endpoint for Arize Phoenix traces. When empty, observability is disabled. Example: `http://phoenix:6006/v1/traces`. |

### Streamlit service (`streamlit`)

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `http://api:8000` | Internal Docker network URL for the FastAPI backend. |
| `API_USERNAME` | `admin` | Username the Streamlit app uses to authenticate with the API. |
| `API_PASSWORD` | `changeme` | Password the Streamlit app uses to authenticate with the API. |

### Phoenix service (`phoenix`)

| Variable | Default | Description |
|----------|---------|-------------|
| `PHOENIX_WORKING_DIR` | `/mnt/data` | Directory inside the Phoenix container where trace data is persisted. |

---

## `.env` File

Create a `.env` file in the project root. Docker Compose reads it automatically via `env_file: [.env]` in the `api` service definition.

```bash
# .env — keep this file out of version control
OPENAI_API_KEY=sk-...
```

Only `OPENAI_API_KEY` must be in `.env`. All other variables have defaults set directly in `docker-compose.yml`.

---

## Production Checklist

- [ ] Set a strong, random `SECRET_KEY` (e.g. `openssl rand -hex 32`).
- [ ] Change `APP_USER` to a non-default username and password.
- [ ] Match `API_USERNAME` / `API_PASSWORD` in the `streamlit` service to the new `APP_USER`.
- [ ] Restrict access to ports 6006 and 8080 (Phoenix and MkDocs) — do not expose them publicly.
- [ ] Use a named volume or a host bind mount with appropriate permissions for `rag_data`.
