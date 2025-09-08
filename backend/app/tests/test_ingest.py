import os
import shutil
import tempfile
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.vectorstore import VectorStore

client = TestClient(app)

def setup_module(_module=None):
    # Fresh tmp dirs
    tmp = tempfile.mkdtemp(prefix="lumina_test_")
    settings.DATA_DIR = tmp
    settings.VECTOR_DIR = os.path.join(tmp, "vectorstore")
    settings.VECTOR_INDEX_PATH = os.path.join(settings.VECTOR_DIR, "store.faiss")
    settings.VECTOR_META_PATH = os.path.join(settings.VECTOR_DIR, "metadata.json")
    settings.DOCS_DIR = os.path.join(tmp, "docs")

    vs = VectorStore.get()
    vs.load_or_initialize()

def teardown_module(_module=None):
    base = os.path.dirname(settings.VECTOR_DIR)
    if os.path.exists(base):
        shutil.rmtree(base, ignore_errors=True)
    # Reset singleton to avoid state bleed across test runs
    VectorStore._instance = None  # noqa

def test_ingest_txt_upload():
    content = b"""Lumina is a self-hosted RAG platform.
It ingests documents, builds embeddings, and answers questions with sources."""
    files = [("files", ("readme.txt", content, "text/plain"))]
    r = client.post("/api/ingest", files=files)
    assert r.status_code == 200
    assert r.json()["status"] == "accepted"

    # Force persist and check index size
    vs = VectorStore.get()
    vs.persist()
    assert vs.index.ntotal > 0
