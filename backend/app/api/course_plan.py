from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embeddings import EmbeddingService
from app.services.vectorstore import VectorStore
from app.services.llm_wrapper import LLMWrapper

router = APIRouter()

embedding_service = EmbeddingService()
vector_store = VectorStore()
llm = LLMWrapper()

class CoursePlanRequest(BaseModel):
    topic: str
    weeks: int = 12

@router.post("/course_plan")
def generate_course_plan(request: CoursePlanRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    # Search for relevant content
    query_emb = embedding_service.embed_text(request.topic)
    results = vector_store.search(query_emb, limit=10)
    sources = [hit.payload.get("text", "") for hit in results]
    
    if not sources:
        return {"course_plan": "No relevant content found for the topic."}
    
    # Prompt for course plan generation
    prompt = f"Generate a {request.weeks}-week course plan for the topic: {request.topic}\n\nBased on the following sources:\n\n" + "\n".join(sources) + "\n\nProvide a structured course plan with weekly topics, objectives, and activities."
    
    course_plan = llm.generate_answer(prompt)
    return {"course_plan": course_plan}
