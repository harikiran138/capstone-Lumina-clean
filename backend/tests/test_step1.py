import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_step1_ingest_and_query():
    """Test Step 1: Ingest text and query the system"""
    # Ingest some content
    ingest_data = {
        "document_id": "math101",
        "text": "In mathematics, the Pythagorean theorem states that in a right-angled triangle, the square of the length of the hypotenuse is equal to the sum of the squares of the other two sides. It is often expressed as a² + b² = c²."
    }
    response = client.post("/api/ingest", json=ingest_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "chunks_indexed" in data
    assert data["chunks_indexed"] > 0

    # Query the ingested content
    query_data = {
        "query": "What does the Pythagorean theorem state?"
    }
    response = client.post("/api/query", json=query_data)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0

    # Verify answer is relevant
    answer = data["answer"].lower()
    assert any(keyword in answer for keyword in ["pythagorean", "theorem", "right-angled", "triangle", "hypotenuse", "a² + b² = c²"])
    print("✅ Step 1 completed successfully")
