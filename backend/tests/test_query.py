import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query():
    # First, ingest the sample documents
    with open("backend/app/sample_data/documents.txt", "rb") as f:
        ingest_response = client.post("/api/ingest", files={"file": ("documents.txt", f, "text/plain")})
    assert ingest_response.status_code == 200

    # Now test queries
    query_expectations = [
        ("What is AI?", "artificial intelligence"),
        ("Explain FastAPI", "fastapi"),
        ("Deep learning basics", "neural networks")
    ]
    for query, expected_keyword in query_expectations:
        response = client.post("/api/query", json={"query": query})
        assert response.status_code == 200
        json_resp = response.json()
        assert "answer" in json_resp
        assert "sources" in json_resp
        # Check that sources are returned
        assert len(json_resp["sources"]) > 0

    # Additional edge case: empty query
    response = client.post("/api/query", json={"query": ""})
    assert response.status_code == 400  # Bad Request

    # Additional edge case: invalid query type
    response = client.post("/api/query", json={"query": 123})
    assert response.status_code == 422  # Unprocessable Entity
