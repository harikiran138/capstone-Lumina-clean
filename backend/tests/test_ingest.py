import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_file():
    # Integration test for ingest endpoint with sample documents.txt
    with open("backend/app/sample_data/documents.txt", "rb") as f:
        response = client.post("/api/ingest", files={"file": ("documents.txt", f, "text/plain")})
    assert response.status_code == 200
    assert "ingested" in response.json()["message"]

def test_ingest_empty_file():
    # Test ingesting an empty file
    response = client.post("/api/ingest", files={"file": ("empty.txt", b"", "text/plain")})
    assert response.status_code == 200  # Assuming it handles empty files gracefully

def test_ingest_invalid_file_type():
    # Test ingesting a non-text file
    response = client.post("/api/ingest", files={"file": ("image.png", b"fake png data", "image/png")})
    assert response.status_code == 200  # Assuming it processes any file as text

def test_health_check():
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
