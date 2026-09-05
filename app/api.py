from fastapi import FastAPI
from app.models import (QuestionRequest)
from app.rag_service import (ask_rag)


app = FastAPI(
    title="Enterprise RAG API",
    version="1.0"
)


@app.get("/")
def root():

    return {
        "message":
            "Enterprise RAG API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    return ask_rag(
        query=request.question,
        user_department=
            request.department.lower()
    )