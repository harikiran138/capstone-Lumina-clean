import os
import uuid
from typing import List, Tuple
from fastapi import UploadFile
from app.core.vectorstore import VectorStore
from app.core.config import settings

from io import BytesIO

# Parsers
from pypdf import PdfReader
try:
    from docx import Document as DocxDocument
    _DOCX_OK = True
except ImportError:
    _DOCX_OK = False

SUPPORTED_EXTS = {".txt", ".md", ".pdf", ".docx"}

class IngestionService:
    def __init__(self):
        os.makedirs(settings.DOCS_DIR, exist_ok=True)
        self.vs = VectorStore.get()

    async def ingest_files(self, files: List[UploadFile]):
        for f in files:
            # Save file to disk
            fname = self._safe_filename(f.filename)
            fpath = os.path.join(settings.DOCS_DIR, fname)
            content = await f.read()
            with open(fpath, "wb") as out:
                out.write(content)

            text = self._extract_text(fname, content)
            chunks = self._chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
            metas = []
            texts = []
            doc_id = str(uuid.uuid4())
            for i, ch in enumerate(chunks):
                texts.append(ch)
                metas.append({
                    "id": f"{doc_id}:{i}",
                    "text": ch,
                    "source": fname,
                    "chunk_id": i,
                    "extra": {"doc_id": doc_id}
                })
            if texts:
                self.vs.add_texts(texts, metas)

        # Persist after batch
        self.vs.persist()

    def _safe_filename(self, name: str) -> str:
        name = os.path.basename(name or "upload")
        if not name:
            name = "upload"
        return name.replace(" ", "_")

    def _extract_text(self, filename: str, raw: bytes) -> str:
        ext = os.path.splitext(filename.lower())[1]
        if ext not in SUPPORTED_EXTS:
            return ""
        if ext in (".txt", ".md"):
            return raw.decode("utf-8", errors="ignore")
        if ext == ".pdf":
            reader = PdfReader(BytesIO(raw))
            pages = []
            for p in reader.pages:
                try:
                    pages.append(p.extract_text() or "")
                except Exception:
                    pages.append("")
            return "\n".join(pages)
        if ext == ".docx" and _DOCX_OK:
            fd = BytesIO(raw)
            doc = DocxDocument(fd)
            paras = [p.text for p in doc.paragraphs]
            return "\n".join(paras)
        return ""

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Simple, fast splitter:
        - Split by paragraphs, then re-pack into ~chunk_size windows with overlap.
        """
        lines = [ln.strip() for ln in text.splitlines()]
        pars = []
        buf = []
        for ln in lines:
            if not ln:
                if buf:
                    pars.append(" ".join(buf).strip())
                    buf = []
            else:
                buf.append(ln)
        if buf:
            pars.append(" ".join(buf).strip())

        # Pack paragraphs into chunks
        chunks: List[str] = []
        curr = ""
        for p in pars:
            if len(curr) + len(p) + 1 <= chunk_size:
                curr = (curr + " " + p).strip()
            else:
                if curr:
                    chunks.append(curr)
                # start new
                curr = p[:chunk_size]
        if curr:
            chunks.append(curr)

        if overlap > 0 and len(chunks) > 1:
            overlapped = []
            prev_tail = ""
            for i, ch in enumerate(chunks):
                if i > 0 and prev_tail:
                    merged = (prev_tail + " " + ch).strip()
                    overlapped.append(merged[:chunk_size])
                else:
                    overlapped.append(ch)
                prev_tail = ch[-overlap:]
            chunks = overlapped

        # Filter tiny chunks
        return [c for c in chunks if len(c) > 30]
