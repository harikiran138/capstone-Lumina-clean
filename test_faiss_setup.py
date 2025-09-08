from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example text
texts = [
    "Artificial Intelligence is transforming education.",
    "FastAPI is a modern Python web framework.",
    "Vector databases store embeddings for semantic search."
]

# Generate embeddings
embeddings = model.encode(texts, convert_to_tensor=False)
print(embeddings.shape)  # (3, 384) -> 3 docs, 384-dim embeddings

# Convert embeddings to numpy
embeddings_np = np.array(embeddings).astype("float32")

# Dimension of embeddings
dim = embeddings_np.shape[1]

# Create FAISS index
index = faiss.IndexFlatL2(dim)

# Add embeddings to index
index.add(embeddings_np)

print("Total vectors in index:", index.ntotal)

# Query
query = "How is AI used in classrooms?"
query_embedding = model.encode([query], convert_to_tensor=False).astype("float32")

# Search top 2 similar vectors
k = 2
distances, indices = index.search(query_embedding, k)

print("Results:")
for idx, dist in zip(indices[0], distances[0]):
    print(f"Text: {texts[idx]} | Distance: {dist}")
