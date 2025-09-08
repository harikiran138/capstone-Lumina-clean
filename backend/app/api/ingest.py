from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
from app.services.ingestion_service import IngestionService

router = APIRouter(tags=["ingest"])

@router.post("/ingest")
async def ingest_files(
    background: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    # Process in background to keep response snappy
    svc = IngestionService()
    background.add_task(svc.ingest_files, files)

    return {"status": "accepted", "num_files": len(files)}
