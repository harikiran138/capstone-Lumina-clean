from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.embeddings import EmbeddingService
from app.services.vectorstore import VectorStore
import hashlib
import time

router = APIRouter()

embedding_service = EmbeddingService()
vector_store = VectorStore()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start >= len(text):
            break
    return chunks

@router.post("/train")
async def train_model(file: UploadFile = File(...)):
    # Placeholder for training logic
    # For now, ingest the file as training data
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    content = await file.read()
    text = content.decode("utf-8")
    if not text.strip():
        return {"message": f"Training file '{file.filename}' is empty."}
    
    chunks = chunk_text(text)
    if not chunks:
        return {"message": f"Training file '{file.filename}' could not be chunked."}
    
    embeddings = embedding_service.embed_texts(chunks)
    points = []
    timestamp = int(time.time())
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        id_str = f"train_{file.filename}_{i}_{timestamp}"
        id_hash = int(hashlib.md5(id_str.encode()).hexdigest(), 16) % (10**9)
        points.append({
            "id": id_hash,
            "vector": emb,
            "payload": {
                "text": chunk,
                "filename": file.filename,
                "chunk_index": i,
                "timestamp": timestamp,
                "type": "training"
            }
        })
    vector_store.upsert(points)
    return {"message": f"Training data from '{file.filename}' ingested with {len(chunks)} chunks."}
