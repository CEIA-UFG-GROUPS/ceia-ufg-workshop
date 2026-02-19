import asyncio
import os
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/api_autoreg_uploads"))
VECTORSTORE_DIR = Path(os.getenv("VECTORSTORE_DIR", "/tmp/api_autoreg_vectorstore"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SUPPORTED_EXTENSIONS = {".pdf", ".txt"}
_vs_lock = asyncio.Lock()

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def _load_users() -> dict[str, str]:
    raw = os.getenv("APP_USER", "admin:secret")
    username, _, password = raw.partition(":")
    return {username: pwd_context.hash(password)}


USERS: dict[str, str] = _load_users()


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_user_hash(username: str) -> str | None:
    return USERS.get(username)


def create_access_token(subject: str) -> tuple[str, int]:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": subject, "exp": expire, "iat": datetime.now(timezone.utc)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return token, ACCESS_TOKEN_EXPIRE_MINUTES * 60


def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    sub = payload.get("sub")
    if sub is None:
        raise JWTError("Missing subject")
    return sub


app = FastAPI(
    title="Document API",
    description="""
## Document API

Receives one or more uploaded documents, saves them, and builds a RAG index with LangChain + OpenAI.

### Features
- Upload **multiple documents** in a single request (PDF and TXT supported for RAG)
- Supports retrieval-augmented generation via `/rag/query`
- Health check endpoint for container orchestration
""",
    version="1.0.0",
    contact={
        "name": "SEFAZ API Team",
    },
    license_info={
        "name": "MIT",
    },
)

# ---------------------------------------------------------------------------
# Observability — Arize Phoenix via OpenTelemetry
# Enabled only when PHOENIX_COLLECTOR_ENDPOINT is set (no-op in tests/local)
# ---------------------------------------------------------------------------
_PHOENIX_ENDPOINT = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "")
if _PHOENIX_ENDPOINT:
    from phoenix.otel import register
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    _tracer_provider = register(
        project_name="api-autoreg",
        endpoint=_PHOENIX_ENDPOINT,
        batch=True,
    )
    FastAPIInstrumentor.instrument_app(app, tracer_provider=_tracer_provider)


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class DocumentsResponse(BaseModel):
    documents: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"documents": ["report.pdf", "invoice.xlsx", "contract.docx"]}
            ]
        }
    }


class HealthResponse(BaseModel):
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"status": "ok"}]
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]


class IndexedDocumentsResponse(BaseModel):
    documents: List[str]


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    exc = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = decode_access_token(token)
    except JWTError:
        raise exc
    if get_user_hash(username) is None:
        raise exc
    return username


# ---------------------------------------------------------------------------
# RAG helpers (sync — called via asyncio.to_thread to avoid blocking the loop)
# ---------------------------------------------------------------------------

def _ingest_file(path: Path) -> int:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS

    if path.suffix == ".pdf":
        loader = PyPDFLoader(str(path))
    else:
        loader = TextLoader(str(path), encoding="utf-8")

    docs = loader.load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150
    ).split_documents(docs)
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    index_file = VECTORSTORE_DIR / "index.faiss"
    if index_file.exists():
        vs = FAISS.load_local(
            str(VECTORSTORE_DIR), embeddings, allow_dangerous_deserialization=True
        )
        vs.add_documents(chunks)
    else:
        vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(str(VECTORSTORE_DIR))
    return len(chunks)


def _run_rag_query(question: str) -> dict | None:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_community.vectorstores import FAISS
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    index_file = VECTORSTORE_DIR / "index.faiss"
    if not index_file.exists():
        return None
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vs = FAISS.load_local(
        str(VECTORSTORE_DIR), embeddings, allow_dangerous_deserialization=True
    )
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=OPENAI_API_KEY,
        temperature=0,
    )
    prompt = ChatPromptTemplate.from_messages([
        ("human", "Answer the question based on the following context:\n\n{context}\n\nQuestion: {question}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    source_docs = retriever.invoke(question)
    sources = list({doc.metadata.get("source", "unknown") for doc in source_docs})

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    answer = chain.invoke(question)
    return {"answer": answer, "sources": sources}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the current health status of the API. Used by Docker and load balancers to verify the service is running.",
    tags=["Monitoring"],
    responses={
        200: {"description": "Service is healthy"},
    },
)
async def health():
    return {"status": "ok"}


@app.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Login",
    tags=["Auth"],
    responses={
        200: {"description": "JWT access token"},
        401: {"description": "Invalid credentials"},
    },
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    stored = get_user_hash(form_data.username)
    if stored is None or not verify_password(form_data.password, stored):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token, expires_in = create_access_token(form_data.username)
    return TokenResponse(access_token=token, token_type="bearer", expires_in=expires_in)


@app.post(
    "/documents",
    response_model=DocumentsResponse,
    summary="Upload Documents",
    description="""
Upload one or more documents. Files are saved to disk and indexed for RAG (PDF and TXT only).

**Accepted formats for indexing:** PDF, TXT

**Request:** `multipart/form-data` with one or more `files` fields.

**Response:** JSON array with the filename of each uploaded document.
""",
    tags=["Documents"],
    responses={
        200: {"description": "List of uploaded document names"},
        422: {"description": "Validation error — no files provided"},
    },
)
async def receive_documents(
    files: List[UploadFile] = File(..., description="One or more documents to upload"),
    current_user: str = Depends(get_current_user),
):
    saved = []
    async with _vs_lock:
        for file in files:
            suffix = Path(file.filename).suffix.lower()
            try:
                dest = UPLOAD_DIR / file.filename
                with dest.open("wb") as f:
                    shutil.copyfileobj(file.file, f)
                if suffix in SUPPORTED_EXTENSIONS and OPENAI_API_KEY:
                    await asyncio.to_thread(_ingest_file, dest)
            except Exception:
                pass  # ingestion failure does not fail the upload response
            saved.append(file.filename)
    return {"documents": saved}


@app.post(
    "/rag/query",
    response_model=QueryResponse,
    summary="Query indexed documents",
    description="Ask a question about the indexed documents using RAG (LangChain + OpenAI).",
    tags=["RAG"],
    responses={
        200: {"description": "Answer and source documents"},
        404: {"description": "No documents indexed yet"},
    },
)
async def rag_query(
    body: QueryRequest,
    current_user: str = Depends(get_current_user),
):
    result = await asyncio.to_thread(_run_rag_query, body.question)
    if result is None:
        raise HTTPException(status_code=404, detail="No documents indexed yet.")
    return result


@app.get(
    "/rag/documents",
    response_model=IndexedDocumentsResponse,
    summary="List indexed documents",
    description="Returns the unique document names currently stored in the FAISS index.",
    tags=["RAG"],
    responses={
        200: {"description": "List of indexed document filenames"},
    },
)
async def list_indexed_documents(
    current_user: str = Depends(get_current_user),
):
    index_file = VECTORSTORE_DIR / "index.faiss"
    if not index_file.exists():
        return {"documents": []}
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vs = FAISS.load_local(
        str(VECTORSTORE_DIR), embeddings, allow_dangerous_deserialization=True
    )
    names = sorted(
        {Path(doc.metadata.get("source", "unknown")).name for doc in vs.docstore._dict.values()}
    )
    return {"documents": names}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
