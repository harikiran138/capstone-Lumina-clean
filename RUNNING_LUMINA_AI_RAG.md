# 🚀 Complete Instructions for Running Lumina AI RAG

## 1️⃣ Start the Backend (FastAPI)

Open a terminal inside `/backend` and run:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

* You should see logs like:

  ```
  INFO:     Uvicorn running on http://0.0.0.0:8000
  INFO:     Application startup complete.
  ```

* In **GitHub Codespaces**, open:

  ```
  https://<your-codespace-name>-8000.app.github.dev/docs
  ```

  (This is the Swagger UI for testing APIs directly.)

👉 Test ingestion works via Swagger:

* Open `/api/ingest` endpoint.
* Upload text.
* Confirm it returns **200 OK**.

---

## 2️⃣ Start the Frontend (React)

Open another terminal inside `/frontend`:

```bash
cd frontend
npm install   # run once
npm run dev
```

* You’ll see output like:

  ```
  VITE vX.X.X ready in 2s
  ➜  Local:   http://localhost:5173
  ➜  Network: http://0.0.0.0:5173
  ```

* In **Codespaces**, open:

  ```
  https://<your-codespace-name>-5173.app.github.dev
  ```

This is your **frontend UI**.

---

## 3️⃣ Fix API URL (important for upload and query)

The upload or query may fail because frontend can’t reach backend.

👉 Open `frontend/src/api.js` and set the API base URL:

```js
// For local machine
const API_BASE = "http://localhost:8000/api";

// For GitHub Codespaces
// const API_BASE = "https://<your-codespace-name>-8000.app.github.dev/api";

export default API_BASE;
```

Save and restart frontend with:

```bash
npm run dev
```

---

## 4️⃣ Upload a Document

In the frontend UI:

* Go to **Upload Docs** tab.
* Select a `.txt` or `.pdf` file.
* Click **Upload**.

Check backend logs — you should see:

```
INFO: Ingested 5 chunks from your-file.txt
```

If you see this, ingestion succeeded ✅.

---

## 5️⃣ Ask Questions

Go to **Chat** tab:

* Type a question, e.g.:

  *“What does the Pythagorean theorem state?”*

* Backend will log something like:

  ```
  INFO: Query: What does the Pythagorean theorem state?
  ```

* AI will respond with an answer from your uploaded file.

---

## 6️⃣ Common Errors & Fixes

### ❌ Upload failed

* **Cause**: Frontend points to `0.0.0.0`.
* **Fix**: Update API\_BASE as explained in Step 3.

### ❌ Cannot connect to `0.0.0.0:8000`

* **Cause**: Browsers cannot resolve `0.0.0.0`.
* **Fix**: Use `localhost` (if local) or `<codespace-name>-8000.app.github.dev` (if in Codespaces).

### ❌ Bad Request (400) on ingest

* **Cause**: Wrong JSON schema.
* **Fix**: Ensure request body looks like:

  ```json
  {
    "document_id": "math101",
    "text": "This is the content of the document..."
  }
  ```

---

✅ If you follow these steps, you’ll be able to:

* Run backend + frontend
* Upload docs successfully
* Ask questions about them
