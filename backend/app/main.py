from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.ingest import router as ingest_router
from .api.query import router as query_router
from .api.train import router as train_router
from .api.test import router as test_router
from .api.course_plan import router as course_plan_router
from config.settings import settings

app = FastAPI(title=settings.app_name, version="1.0.0")

# CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(ingest_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(train_router, prefix="/api")
app.include_router(test_router, prefix="/api")
app.include_router(course_plan_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.backend_host, port=settings.backend_port)
