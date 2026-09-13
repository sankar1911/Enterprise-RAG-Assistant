import os

import requests
import streamlit as st


FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="RAG Assistant",
    layout="wide"
)


st.title(
    "RAG Assistant"
)

st.write(
    "Upload PDF documents and ask questions from them."
)


st.subheader(
    "Documents"
)


uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button("Process Documents"):
    if not uploaded_files:
        st.warning(
            "Please upload at least one PDF."
        )

    else:
        files = [
            (
                "files",
                (
                    file.name,
                    file.getvalue(),
                    "application/pdf"
                )
            )
            for file in uploaded_files
        ]

        try:
            with st.spinner(
                "Processing documents..."
            ):
                response = requests.post(
                    f"{FASTAPI_URL}/upload",
                    files=files,
                    timeout=300
                )

            data = response.json()

            if data.get("success"):
                st.success(
                    "Documents processed successfully."
                )

                st.write(
                    "**Uploaded:**",
                    len(data["uploaded_files"])
                )

                st.write(
                    "**Total documents:**",
                    data["total_documents"]
                )

                st.write(
                    "**Total chunks:**",
                    data["total_chunks"]
                )

            else:
                st.error(
                    data.get(
                        "message",
                        "Document processing failed."
                    )
                )

        except requests.RequestException as error:
            st.error(
                f"Backend connection failed: {error}"
            )


st.divider()


st.subheader(
    "Ask a Question"
)


question = st.text_input(
    "Enter your question"
)


if st.button("Ask"):
    if not question.strip():
        st.warning(
            "Please enter a question."
        )

    else:
        try:
            with st.spinner(
                "Searching documents..."
            ):
                response = requests.post(
                    f"{FASTAPI_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=180
                )

            data = response.json()

            st.subheader(
                "Answer"
            )

            st.write(
                data["answer"]
            )

            st.write(
                "**Confidence:**",
                data["confidence"]
            )

            if data.get("sources"):
                st.subheader(
                    "Sources"
                )

                for source in data["sources"]:
                    st.write(
                        f"""
**File:** {source['file']}  
**Page:** {source['page']}  
**Chunk ID:** {source['chunk_id']}  
**Rerank Score:** {source['rerank_score']:.4f}
"""
                    )

        except requests.RequestException as error:
            st.error(
                f"Backend connection failed: {error}"
            )