<<<<<<< HEAD
# capstone-Lumina-clean
=======
# Lumina

Lumina is a self-hosted **AI RAG (Retrieval-Augmented Generation) platform** that transforms raw documents (like textbooks and syllabi) into structured, queryable knowledge. It uses local embeddings, a vector database, and a self-hosted LLM to let students and educators upload content, ask questions, and receive accurate, source-backed answers.

---

## Project Structure

```
lumina/
# Lumina

Lumina is a self-hosted **AI RAG (Retrieval-Augmented Generation) platform** that transforms raw documents (like textbooks and syllabi) into structured, queryable knowledge. It uses local embeddings, a vector database, and a self-hosted LLM to let students and educators upload content, ask questions, and receive accurate, source-backed answers.

---

## Project Structure

```
lumina/
├─ backend/          # FastAPI backend
│  ├─ app/
│  │  ├─ main.py     # App entrypoint
│  │  ├─ services/   # Core logic (embeddings, vector DB, LLM)
│  │  │  ├─ embeddings.py
│  │  │  ├─ vectorstore.py
│  │  │  ├─ llm_wrapper.py
│  │  ├─ api/        # REST endpoints (ingest, query)
│  │  │  ├─ ingest.py
│  │  │  ├─ query.py
│  ├─ tests/         # Backend unit tests
│  │  ├─ test_ingest.py
│  │  ├─ test_query.py
│  ├─ config/        # Settings and env management
│  │  ├─ settings.py
│  ├─ requirements.txt
│  ├─ Dockerfile
├─ frontend/         # React (Vite + Tailwind) frontend
│  ├─ src/
│  │  ├─ components/ # Chat and Upload components
│  │  │  ├─ Chat.jsx
│  │  │  ├─ Upload.jsx
│  │  ├─ App.jsx
│  │  ├─ main.jsx
│  │  ├─ index.html
│  ├─ public/        # Static assets
│  ├─ package.json
│  ├─ Dockerfile
├─ data/             # Uploaded docs and embeddings
├─ docs/             # Documentation
│  ├─ architecture.md
│  ├─ runbook.md
├─ scripts/          # Helper scripts (setup, seed)
│  ├─ setup.sh
│  ├─ seed_data.py
├─ docker-compose.yml
├─ .env.example      # Example config variables
├─ README.md
```

---

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/lumina.git
   cd lumina
   ```

2. Create a `.env` file from `.env.example` and set environment variables.

3. Start services with Docker:

   ```bash
   docker-compose up --build
   ```

4. Access:

   * Backend API → `http://localhost:8000`
   * Frontend UI → `http://localhost:5173`
   * Qdrant (vector DB) → `http://localhost:6333`

---

## Usage

* Upload files for ingestion (via UI or `/ingest` API).
* Query the system in the chat interface.
* Answers include **source references** from ingested docs.

---

## Development Notes

* Backend: FastAPI on port 8000.
* Frontend: Vite + React on port 5173.
* Vector DB: Qdrant on port 6333 (default).
* Run tests:

  ```bash
  cd backend
  pytest
  ```

---

## Next Steps

* Implement feedback loop (thumbs up/down on answers).
* Add authentication and role-based access.
* Deploy with Kubernetes for scalability.
