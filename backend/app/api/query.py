from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.query_service import QueryService

router = APIRouter(tags=["query"])

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(5, ge=1, le=50)
    max_context_tokens: int = Field(1200, ge=256, le=4096)

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    svc = QueryService()
    answer, sources = svc.answer_query(
        query=req.query,
        top_k=req.top_k,
        max_context_tokens=req.max_context_tokens
    )
    return QueryResponse(answer=answer, sources=sources)
