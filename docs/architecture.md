# Lumina Architecture

## Overview
Lumina is a self-hosted AI RAG (Retrieval-Augmented Generation) application that allows users to upload documents, query them, and receive AI-generated answers with sources.

## Components
- **Backend**: FastAPI server handling ingestion and querying.
- **Frontend**: React app for user interaction.
- **Vector Database**: Qdrant for storing embeddings.
- **Embeddings**: Sentence Transformers for text embeddings.
- **LLM**: Placeholder for local LLM integration.

## Data Flow
1. User uploads file via frontend.
2. Backend chunks text, embeds, stores in Qdrant.
3. User queries via frontend.
4. Backend retrieves relevant chunks, sends to LLM, returns answer.
