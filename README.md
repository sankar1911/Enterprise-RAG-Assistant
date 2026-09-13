# Multi-Document RAG Assistant

A secure multi-document Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF documents and ask questions grounded in the uploaded content.

The system uses sentence-transformer embeddings, FAISS vector search, hybrid retrieval, CrossEncoder reranking, document guardrails, and Gemini for answer generation.

## Features

- Upload and process multiple PDF documents
- Extract page-level text using PyMuPDF
- Sentence-aware chunking with overlap
- Generate embeddings using `all-MiniLM-L6-v2`
- Store and search vectors using FAISS
- Hybrid semantic and keyword retrieval
- CrossEncoder reranking for improved relevance
- Source tracking with file name, page number, and chunk ID
- Prompt-injection detection for user queries
- Retrieved-document safety filtering
- Gemini primary and fallback model support
- Retry handling for temporary API failures
- Confidence handling for retrieved answers
- FastAPI backend
- Streamlit frontend

## Architecture

```text
Multiple PDF Documents
        |
        v
     PyMuPDF
        |
        v
 Text Cleaning
        |
        v
Sentence-Aware Chunking
   + Chunk Overlap
        |
        v
Sentence Transformer
     Embeddings
        |
        v
     FAISS Index
        |
        +----------------------+
                               |
User Question                  |
     |                         |
     v                         |
Query Validation               |
     |                         |
     v                         |
Query Embedding                |
     |                         |
     v                         |
Hybrid Retrieval <-------------+
     |
     v
CrossEncoder Reranking
     |
     v
Top Relevant Chunks
     |
     v
Document Guardrail
     |
     v
Safe Context
     |
     v
Gemini Primary Model
     |
     +---- failure ----> Gemini Fallback Model
     |
     v
Grounded Answer
     |
     v
Answer + Sources + Confidence
```

## Project Structure

```text
Secure-Multi-Document-RAG-Assistant/
│
├── app/
│   ├── api.py
│   ├── chunking.py
│   ├── document_service.py
│   ├── embeddings.py
│   ├── guardrails.py
│   ├── loaders.py
│   ├── models.py
│   ├── rag_service.py
│   ├── reranker.py
│   └── retrieval.py
│
├── data/
│   ├── uploads/
│   └── index/
│
├── streamlit_app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## RAG Pipeline

### 1. Document Loading

PDF documents are loaded using PyMuPDF.

Each page is extracted with:

- page number
- page text
- file name metadata

### 2. Chunking

The extracted text is cleaned and divided into sentence-aware chunks.

The chunker:

- preserves sentence boundaries where possible
- limits chunk size
- keeps overlap between neighbouring chunks
- preserves source metadata

Example:

```text
Chunk 1:
A + B + C

Chunk 2:
C + D + E
```

The repeated content helps preserve context across chunk boundaries.

### 3. Embeddings

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Document chunks are converted into dense vector embeddings.

The same embedding model is used for user queries.

### 4. FAISS Vector Search

Document embeddings are stored in a FAISS index.

The index is persisted to disk so document embeddings do not need to be recreated for every user question.

At query time, only the user question is embedded.

### 5. Hybrid Retrieval

The retrieval layer combines:

- semantic similarity from FAISS
- keyword matching

This improves retrieval when exact keywords and semantic meaning are both useful.

### 6. CrossEncoder Reranking

The first-stage retrieval returns candidate chunks.

A CrossEncoder then compares each query/chunk pair:

```text
query + candidate chunk -> relevance score
```

Model:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The highest-scoring chunks are passed to the generation stage.

### 7. Guardrails

The application contains multiple safety checks.

#### User Input Guardrail

Checks:

- empty queries
- invalid input
- excessive query length
- suspicious prompt-injection patterns

#### Retrieved Document Guardrail

Retrieved chunks are checked before being sent to Gemini.

Suspicious instructions inside uploaded documents can be filtered out.

#### Output Validation

The generated answer is checked before it is returned to the user.

### 8. Gemini Generation

Gemini receives only the selected document context.

The model is instructed to:

- answer only from retrieved document content
- avoid outside knowledge
- avoid inventing facts
- combine information from multiple retrieved passages when necessary
- return an insufficient-information response when the answer is not supported by the documents

The application supports a primary and fallback Gemini model.

Example:

```env
GEMINI_MODEL=gemini-3.8-flash
GEMINI_FALLBACK_MODEL=gemini-3.5-flash-lite
```

Temporary failures such as `429`, `500`, `502`, `503`, and `504` can be retried before switching to the fallback model.



## Running the Application

### Start FastAPI

```bash
uvicorn app.api:app --reload
```

FastAPI will normally run at:

```text
http://127.0.0.1:8000
```

### Start Streamlit

Open another terminal:

```bash
streamlit run streamlit_app.py
```

Streamlit will normally run at:

```text
http://localhost:8501
```



## Technologies Used

- Python
- FastAPI
- Streamlit
- PyMuPDF
- Sentence Transformers
- FAISS
- CrossEncoder
- Gemini API
- NumPy
- Requests
- Pydantic
- Regular Expressions

## Skills Demonstrated

This project demonstrates experience with:

- Retrieval-Augmented Generation
- Multi-document ingestion
- PDF text extraction
- Text cleaning and chunking
- Chunk overlap
- Embedding generation
- Vector databases and FAISS
- Semantic search
- Hybrid retrieval
- CrossEncoder reranking
- Prompt engineering
- Prompt-injection protection
- Document-context guardrails
- LLM fallback and retry handling
- FastAPI backend development
- Streamlit application development
- Source attribution
- RAG debugging and evaluation


