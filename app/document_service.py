import json
from pathlib import Path

import faiss

from app.loaders import load_pdf
from app.chunking import create_chunks
from app.embeddings import create_embeddings
from app.retrieval import create_faiss_index


UPLOAD_DIR = Path("data/uploads")
INDEX_DIR = Path("data/index")

INDEX_PATH = INDEX_DIR / "documents.faiss"
CHUNKS_PATH = INDEX_DIR / "chunks.json"


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INDEX_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def build_document_index():
    all_chunks = []
    pdf_files = sorted(
        UPLOAD_DIR.glob("*.pdf")
    )

    for pdf_path in pdf_files:
        pages = load_pdf(
            str(pdf_path)
        )

        document_chunks = create_chunks(
            pages,
            pdf_path.name
        )

        all_chunks.extend(
            document_chunks
        )

    if not all_chunks:
        return {
            "documents": 0,
            "chunks": 0
        }

    for chunk_id, chunk in enumerate(
        all_chunks
    ):
        chunk["chunk_id"] = chunk_id

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = create_embeddings(texts)

    index = create_faiss_index(embeddings)

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(
        CHUNKS_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            all_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    return {
        "documents": len(pdf_files),
        "chunks": len(all_chunks)
    }


def load_document_index():
    if not INDEX_PATH.exists():
        return None, []

    if not CHUNKS_PATH.exists():
        return None, []

    index = faiss.read_index(
        str(INDEX_PATH)
    )
    with open(
        CHUNKS_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    return index, chunks