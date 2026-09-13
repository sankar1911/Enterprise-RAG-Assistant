import shutil
from pathlib import Path
from fastapi import (FastAPI,UploadFile,File)
from app.models import QuestionRequest
from app.rag_service import ask_rag
from app.document_service import (UPLOAD_DIR,build_document_index)


app = FastAPI(title="RAG Assistant API",
    version="2.0"
)


@app.get("/")
def root():
    return {
        "message": "RAG Assistant API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/upload")
def upload_documents(
    files: list[UploadFile] = File(...)
):
    uploaded_files = []

    for file in files:
        file_name = Path(file.filename or "").name

        if not file_name.lower().endswith(".pdf"):
            continue

        file_path = ( UPLOAD_DIR / file_name)

        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        uploaded_files.append(file_name)

    if not uploaded_files:
        return {
            "success": False,
            "message": "No valid PDF files were uploaded."
        }

    result = build_document_index()

    return {
        "success": True,
        "uploaded_files": uploaded_files,
        "total_documents": result["documents"],
        "total_chunks": result["chunks"]
    }


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):
    return ask_rag(
        request.question
    )