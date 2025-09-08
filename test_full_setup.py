from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load sample text
with open("backend/app/sample_data/documents.txt", "r") as f:
    docs = f.readlines()

# Strip whitespace
docs = [doc.strip() for doc in docs if doc.strip()]

print(f"Loaded {len(docs)} documents:")
for i, doc in enumerate(docs):
    print(f"{i+1}. {doc}")

# Generate embeddings
embeddings = model.encode(docs, convert_to_tensor=False).astype("float32")

print(f"\nEmbeddings shape: {embeddings.shape}")

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

print(f"FAISS index created with {index.ntotal} vectors")

# Test queries
queries = [
    "What is AI?",
    "Tell me about machine learning",
    "How do neural networks work?"
]

for query in queries:
    print(f"\nQuery: {query}")
    query_embedding = model.encode([query], convert_to_tensor=False).astype("float32")
    distances, indices = index.search(query_embedding, k=2)
    
    print("Top 2 results:")
    for idx, dist in zip(indices[0], distances[0]):
        print(f"  Text: {docs[idx]} | Distance: {dist:.4f}")
