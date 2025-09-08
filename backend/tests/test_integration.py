import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import tempfile

client = TestClient(app)

def test_full_workflow_text_file():
    """Test complete workflow: upload text file, query, get accurate answer"""
    # Use sample data file
    sample_file_path = "backend/app/sample_data/documents.txt"

    # Ensure sample file exists
    assert os.path.exists(sample_file_path), "Sample documents.txt file not found"

    # Step 1: Upload/ingest the document
    with open(sample_file_path, "rb") as f:
        response = client.post("/api/ingest", files={"file": ("documents.txt", f, "text/plain")})

    assert response.status_code == 200
    data = response.json()
    assert "ingested" in data["message"].lower()

    # Step 2: Query the system
    query_data = {"query": "What is machine learning?"}
    response = client.post("/api/query", json=query_data)

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0

    # Verify answer is relevant
    answer = data["answer"].lower()
    assert any(keyword in answer for keyword in ["machine learning", "ml", "algorithm", "data"])

def test_pdf_upload_workflow():
    """Test PDF upload and text extraction"""
    # Create a simple PDF content for testing
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Machine Learning Basics) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000200 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n284\n%%EOF"

    # Step 1: Upload PDF
    response = client.post("/api/ingest", files={"file": ("test.pdf", pdf_content, "application/pdf")})

    assert response.status_code == 200
    data = response.json()
    assert "ingested" in data["message"].lower()

    # Step 2: Query about PDF content
    query_data = {"query": "What is machine learning?"}
    response = client.post("/api/query", json=query_data)

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_empty_file_handling():
    """Test handling of empty files"""
    response = client.post("/api/ingest", files={"file": ("empty.txt", b"", "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert "empty" in data["message"].lower() or "whitespace" in data["message"].lower()

def test_invalid_file_type():
    """Test handling of unsupported file types"""
    response = client.post("/api/ingest", files={"file": ("image.png", b"fake png data", "image/png")})
    # Should still process as text
    assert response.status_code == 200

def test_query_without_documents():
    """Test querying when no documents are ingested"""
    # This test might fail if documents persist between tests
    # In a real scenario, we'd want to clear the vector store
    query_data = {"query": "test query"}
    response = client.post("/api/query", json=query_data)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    # Answer might be empty or generic when no documents are available

def test_multiple_queries():
    """Test multiple queries to verify system stability"""
    queries = [
        "What is AI?",
        "Explain machine learning",
        "What are neural networks?"
    ]

    for query in queries:
        response = client.post("/api/query", json={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
