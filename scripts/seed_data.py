#!/usr/bin/env python3
"""
Seed data script for Lumina.
This script can be used to populate the vector database with sample data for testing.
"""

from backend.app.services.embeddings import EmbeddingService
from backend.app.services.vectorstore import VectorStore

def seed_sample_data():
    embedding_service = EmbeddingService()
    vector_store = VectorStore()

    sample_texts = [
        "Lumina is a self-hosted AI RAG platform.",
        "It uses local embeddings and vector databases.",
        "Users can upload documents and ask questions.",
        "Answers are generated based on ingested content."
    ]

    embeddings = embedding_service.embed_texts(sample_texts)
    points = []
    for i, emb in enumerate(embeddings):
        points.append({
            "id": i,
            "vector": emb,
            "payload": {"text": sample_texts[i]}
        })

    vector_store.upsert(points)
    print(f"Seeded {len(points)} sample points.")

if __name__ == "__main__":
    seed_sample_data()
