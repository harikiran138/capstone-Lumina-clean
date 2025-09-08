from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Paths & persistence
    DATA_DIR: str = "data"
    VECTOR_DIR: str = "data/vectorstore"
    VECTOR_INDEX_PATH: str = "data/vectorstore/store.faiss"
    VECTOR_META_PATH: str = "data/vectorstore/metadata.json"
    DOCS_DIR: str = "data/docs"

    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Chunking
    CHUNK_SIZE: int = 900
    CHUNK_OVERLAP: int = 150

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(env_prefix="LUMINA_", env_file=".env", extra="ignore")

settings = Settings()
