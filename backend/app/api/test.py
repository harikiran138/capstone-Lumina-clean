from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embeddings import EmbeddingService
from app.services.vectorstore import VectorStore
from app.services.llm_wrapper import LLMWrapper
from typing import List, Dict
import numpy as np

router = APIRouter()

embedding_service = EmbeddingService()
vector_store = VectorStore()
llm = LLMWrapper()

class TestQuery(BaseModel):
    query: str
    ground_truth: str

class TestRequest(BaseModel):
    queries: List[TestQuery]
    k: int = 5

def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    return len([r for r in retrieved_k if r in relevant_set]) / k

def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    return len([r for r in retrieved_k if r in relevant_set]) / len(relevant) if relevant else 0

def mrr(retrieved: List[str], relevant: List[str]) -> float:
    relevant_set = set(relevant)
    for i, r in enumerate(retrieved):
        if r in relevant_set:
            return 1 / (i + 1)
    return 0

def answer_accuracy(generated: str, ground_truth: str) -> float:
    # Simple accuracy: 1 if generated contains ground_truth keywords, else 0
    # In practice, use more sophisticated metrics like BLEU, ROUGE
    return 1.0 if ground_truth.lower() in generated.lower() else 0.0

@router.post("/test")
def test_system(request: TestRequest):
    if not request.queries:
        raise HTTPException(status_code=400, detail="No test queries provided")
    
    results = []
    total_precision = 0
    total_recall = 0
    total_mrr = 0
    total_accuracy = 0
    
    for test_query in request.queries:
        query_emb = embedding_service.embed_text(test_query.query)
        search_results = vector_store.search(query_emb, limit=request.k)
        retrieved_texts = [hit.payload.get("text", "") for hit in search_results]
        
        # For simplicity, assume ground_truth is a string, split into relevant docs
        relevant = [test_query.ground_truth]  # In practice, list of relevant texts
        
        precision = precision_at_k(retrieved_texts, relevant, request.k)
        recall = recall_at_k(retrieved_texts, relevant, request.k)
        mrr_val = mrr(retrieved_texts, relevant)
        
        # Generate answer
        sources = retrieved_texts
        prompt = f"Answer the question based on the following sources:\n\n" + "\n".join(sources) + f"\n\nQuestion: {test_query.query}"
        generated_answer = llm.generate_answer(prompt)
        accuracy = answer_accuracy(generated_answer, test_query.ground_truth)
        
        results.append({
            "query": test_query.query,
            "precision@k": precision,
            "recall@k": recall,
            "mrr": mrr_val,
            "answer_accuracy": accuracy
        })
        
        total_precision += precision
        total_recall += recall
        total_mrr += mrr_val
        total_accuracy += accuracy
    
    num_queries = len(request.queries)
    avg_metrics = {
        "avg_precision@k": total_precision / num_queries,
        "avg_recall@k": total_recall / num_queries,
        "avg_mrr": total_mrr / num_queries,
        "avg_answer_accuracy": total_accuracy / num_queries
    }
    
    return {"results": results, "average_metrics": avg_metrics}
