"""
Streamlit Document Q&A Interface
Thin UI that delegates all RAG logic to the FastAPI backend.
"""

import os
import time

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "changeme")

# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def _login() -> dict:
    """Obtain a JWT token from the API and return {token, expires_at}."""
    resp = requests.post(
        f"{API_BASE_URL}/auth/login",
        data={"username": API_USERNAME, "password": API_PASSWORD},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "token": data["access_token"],
        "expires_at": time.time() + data["expires_in"] - 60,  # 60 s safety margin
    }


def _auth_headers() -> dict[str, str]:
    """Return Authorization headers, refreshing the token if needed."""
    if (
        "auth" not in st.session_state
        or time.time() >= st.session_state.auth["expires_at"]
    ):
        st.session_state.auth = _login()
    return {"Authorization": f"Bearer {st.session_state.auth['token']}"}


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def api_upload(files: list) -> list[str]:
    """Upload files to the API; return list of indexed filenames."""
    multipart = [("files", (f.name, f.getvalue(), f.type or "application/octet-stream")) for f in files]
    resp = requests.post(
        f"{API_BASE_URL}/documents",
        files=multipart,
        headers=_auth_headers(),
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["documents"]


def api_list_documents() -> list[str]:
    """Fetch names of documents currently in the FAISS index."""
    resp = requests.get(
        f"{API_BASE_URL}/rag/documents",
        headers=_auth_headers(),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["documents"]


def api_query(question: str) -> dict:
    """Send a RAG query and return {answer, sources}."""
    resp = requests.post(
        f"{API_BASE_URL}/rag/query",
        json={"question": question},
        headers=_auth_headers(),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {role, content, sources?}

# Ensure we have a valid token on first load
try:
    _auth_headers()
except Exception as exc:
    st.error(f"Failed to authenticate with the API: {exc}")
    st.stop()

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Document Q&A", page_icon="📄", layout="wide")
st.title("📄 Document Q&A")

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    if st.button("Upload and Index", disabled=not uploaded_files):
        with st.spinner("Uploading and indexing…"):
            try:
                names = api_upload(uploaded_files)
                st.success(f"Indexed: {', '.join(names)}")
            except requests.HTTPError as e:
                st.error(f"Upload failed: {e.response.text}")
            except Exception as e:
                st.error(f"Upload error: {e}")

    st.divider()
    st.subheader("Indexed Documents")
    try:
        indexed = api_list_documents()
        if indexed:
            for name in indexed:
                st.markdown(f"- {name}")
        else:
            st.caption("No documents indexed yet.")
    except Exception as e:
        st.caption(f"Could not fetch document list: {e}")

# ── Chat area ────────────────────────────────────────────────────────────────

# Render existing chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for src in msg["sources"]:
                    st.markdown(f"- `{src}`")

# New question input
if question := st.chat_input("Ask a question about your documents…"):
    # Show user message immediately
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Call API and stream response
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = api_query(question)
                answer = result["answer"]
                sources = result.get("sources", [])
            except requests.HTTPError as e:
                if e.response.status_code == 404:
                    answer = "No documents have been indexed yet. Please upload a PDF or TXT file first."
                    sources = []
                else:
                    answer = f"API error: {e.response.text}"
                    sources = []
            except Exception as e:
                answer = f"Unexpected error: {e}"
                sources = []

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.markdown(f"- `{src}`")

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
