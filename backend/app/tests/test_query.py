import time
from fastapi.testclient import TestClient
from app.main import app
from app.core.vectorstore import VectorStore

client = TestClient(app)

def test_query_after_ingest():
    # Wait a bit in case background task is still processing
    time.sleep(0.3)
    r = client.post("/api/query", json={"query": "What is Lumina?", "top_k": 3})
    assert r.status_code == 200
    payload = r.json()
    assert "answer" in payload
    assert "sources" in payload
    # If empty KB, answer still returns a helpful message
    assert isinstance(payload["sources"], list)
