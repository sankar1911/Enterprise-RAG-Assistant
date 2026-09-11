# Enterprise RAG Knowledge Assistant

Enterprise document question-answering system using Retrieval-Augmented Generation.

## Features

- PDF ingestion
- Chunking and metadata
- SentenceTransformer embeddings
- FAISS vector search
- Hybrid search
- Cross-Encoder reranking
- Confidence threshold
- Prompt injection guardrails
- Department access control
- GENAI
- Source citations
- FastAPI backend
- Streamlit frontend
- PyTest
- Docker Compose

## Architecture

User
→ Streamlit
→ FastAPI
→ Guardrails
→ Access Control
→ Embeddings
→ FAISS
→ Hybrid Search
→ Cross-Encoder
→ Confidence Check
→ Context Builder
→ GENAI
→ Answer + Citation