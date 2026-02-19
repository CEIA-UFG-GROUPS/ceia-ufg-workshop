# Development

## Prerequisites

| Tool | Purpose |
|------|---------|
| [uv](https://docs.astral.sh/uv/) | Fast Python package and project manager |
| Python 3.13 | Runtime (managed by uv via `.python-version`) |
| Docker + Compose | Running the full stack or individual services |

## Local Setup (without Docker)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create the virtual environment and install all dependencies
uv sync

# Copy and edit the environment file
cp .env.example .env   # or create .env manually with OPENAI_API_KEY=sk-...

# Start the API with hot reload
uv run uvicorn main:app --reload --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## Running Tests

```bash
uv run pytest test_main.py -v
```

Tests use an in-process `TestClient` and do not require a running Docker stack or an OpenAI key (RAG ingestion is skipped when `OPENAI_API_KEY` is empty).

## Hot Reload in Docker

The `api` service in `docker-compose.yml` bind-mounts the project root into `/app`:

```yaml
volumes:
  - .:/app
```

Uvicorn is started with `--reload`, so changes to `main.py` take effect immediately without rebuilding the image.

## Adding Python Dependencies

```bash
# Add a runtime dependency
uv add some-package

# Add a dev-only dependency
uv add --dev some-dev-package
```

After adding packages, rebuild the Docker image to pick up the updated `uv.lock`:

```bash
docker compose build api
```

## Running the Streamlit App Locally

```bash
cd streamlit_app
uv sync
API_BASE_URL=http://localhost:8000 uv run streamlit run app.py
```

## Project Structure

```
api-autoreg/
├── main.py                  # FastAPI application (single-file)
├── test_main.py             # pytest test suite
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependency tree
├── Dockerfile               # API container image
├── docker-compose.yml       # Full stack definition
├── .env                     # Secrets (not committed)
├── .python-version          # Python version pin for uv
├── mkdocs.yml               # MkDocs configuration
├── docs/                    # Documentation source (this site)
│   ├── Dockerfile           # MkDocs container image
│   ├── index.md
│   ├── getting-started.md
│   ├── architecture.md
│   ├── api-reference.md
│   ├── rag-pipeline.md
│   ├── configuration.md
│   └── development.md
└── streamlit_app/
    ├── app.py               # Streamlit UI
    ├── Dockerfile
    ├── pyproject.toml
    └── uv.lock
```

## Linting and Formatting

The project does not currently enforce a specific linter. Adding `ruff` is recommended:

```bash
uv add --dev ruff
uv run ruff check .
uv run ruff format .
```
