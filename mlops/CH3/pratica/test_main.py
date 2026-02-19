import io
import os

os.environ.setdefault("APP_USER", "testuser:testpass")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def make_file(filename: str, content: str = "dummy content"):
    return (filename, io.BytesIO(content.encode()), "application/octet-stream")


def get_valid_token() -> str:
    r = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    return r.json()["access_token"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_single_document():
    response = client.post(
        "/documents",
        files=[("files", make_file("report.pdf"))],
        headers={"Authorization": f"Bearer {get_valid_token()}"},
    )
    assert response.status_code == 200
    assert response.json() == {"documents": ["report.pdf"]}


def test_multiple_documents():
    response = client.post(
        "/documents",
        files=[
            ("files", make_file("report.pdf")),
            ("files", make_file("invoice.xlsx")),
            ("files", make_file("contract.docx")),
        ],
        headers={"Authorization": f"Bearer {get_valid_token()}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "documents": ["report.pdf", "invoice.xlsx", "contract.docx"]
    }


def test_missing_files_returns_422():
    response = client.post(
        "/documents",
        headers={"Authorization": f"Bearer {get_valid_token()}"},
    )
    assert response.status_code == 422


def test_response_contains_documents_key():
    response = client.post(
        "/documents",
        files=[("files", make_file("any.txt"))],
        headers={"Authorization": f"Bearer {get_valid_token()}"},
    )
    assert "documents" in response.json()


def test_document_names_match_uploaded_filenames():
    filenames = ["a.pdf", "b.csv", "c.json"]
    files = [("files", make_file(name)) for name in filenames]
    response = client.post(
        "/documents",
        files=files,
        headers={"Authorization": f"Bearer {get_valid_token()}"},
    )
    assert response.json()["documents"] == filenames


# --- Auth tests ---

def test_login_returns_token():
    r = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert r.status_code == 200
    data = r.json()
    assert data["access_token"] != ""
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800


def test_login_wrong_password_returns_401():
    r = client.post("/auth/login", data={"username": "testuser", "password": "wrongpass"})
    assert r.status_code == 401


def test_login_unknown_user_returns_401():
    r = client.post("/auth/login", data={"username": "nobody", "password": "testpass"})
    assert r.status_code == 401


def test_login_missing_fields_returns_422():
    r = client.post("/auth/login", data={"username": "testuser"})
    assert r.status_code == 422


def test_documents_without_token_returns_401():
    r = client.post("/documents", files=[("files", make_file("doc.pdf"))])
    assert r.status_code == 401


def test_documents_with_invalid_token_returns_401():
    r = client.post(
        "/documents",
        files=[("files", make_file("doc.pdf"))],
        headers={"Authorization": "Bearer this.is.not.a.valid.token"},
    )
    assert r.status_code == 401


def test_documents_with_expired_token_returns_401():
    from datetime import datetime, timedelta, timezone
    from jose import jwt

    past = datetime.now(timezone.utc) - timedelta(hours=1)
    expired_token = jwt.encode(
        {"sub": "testuser", "exp": past, "iat": past},
        "test-secret-key",
        algorithm="HS256",
    )
    r = client.post(
        "/documents",
        files=[("files", make_file("doc.pdf"))],
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert r.status_code == 401


def test_documents_with_tampered_token_returns_401():
    token = get_valid_token()
    parts = token.split(".")
    tampered = parts[0] + "." + parts[1] + ".invalidsignature"
    r = client.post(
        "/documents",
        files=[("files", make_file("doc.pdf"))],
        headers={"Authorization": f"Bearer {tampered}"},
    )
    assert r.status_code == 401


def test_health_still_public_after_auth_added():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
