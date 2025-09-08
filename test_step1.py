"""
Lumina Step 1 Automated Test: Embeddings + Vector DB Validation

Goal: Verify that the Step 1 pipeline works end-to-end.

1. Upload sample documents.
2. Generate embeddings.
3. Store embeddings in FAISS.
4. Run semantic queries.
5. Output a success/failure report.
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -----------------------
# Sample Documents
# -----------------------
docs = [
    "Artificial Intelligence is transforming education worldwide.",
    "FastAPI is a Python web framework for building APIs.",
    "Vector databases allow semantic search over embeddings.",
    "Neural networks are the core of deep learning.",
    "Machine learning can automate decision making."
]

# -----------------------
# Sample Queries and Expected Matches
# -----------------------
test_cases = {
    "What is AI?": "Artificial Intelligence is transforming education worldwide.",
    "Explain FastAPI": "FastAPI is a Python web framework for building APIs.",
    "Deep learning basics": "Neural networks are the core of deep learning."
}

# -----------------------
# Initialize Embedding Model
# -----------------------
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------
# Generate Embeddings
# -----------------------
print("Generating embeddings for sample documents...")
embeddings = model.encode(docs, convert_to_tensor=False).astype("float32")

# -----------------------
# Initialize FAISS Index
# -----------------------
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
print(f"FAISS index created with {index.ntotal} vectors.")

# -----------------------
# Run Test Queries
# -----------------------
print("\nRunning test queries...")
success_count = 0

for query, expected in test_cases.items():
    q_emb = model.encode([query], convert_to_tensor=False).astype("float32")
    distances, indices = index.search(q_emb, k=1)
    matched_doc = docs[indices[0][0]]
    is_correct = matched_doc == expected
    status = "PASS" if is_correct else "FAIL"
    print(f"\nQuery: {query}")
    print(f"Expected Match: {expected}")
    print(f"Retrieved Match: {matched_doc}")
    print(f"Test Result: {status}")
    if is_correct:
        success_count += 1

# -----------------------
# Final Summary
# -----------------------
total_tests = len(test_cases)
print(f"\nStep 1 Test Summary: {success_count}/{total_tests} passed.")
if success_count == total_tests:
    print("✅ Step 1 is fully functional!")
else:
    print("❌ Step 1 has issues. Check embedding generation, FAISS index, or query retrieval.")
