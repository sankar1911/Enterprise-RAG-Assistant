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
- Ollama Qwen2.5:7b
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
→ Ollama Qwen2.5:7b
→ Answer + Citation

## Run Ollama

```bash
ollama run qwen2.5:7b