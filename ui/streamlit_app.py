import streamlit as st
import requests
import os

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="Enterprise RAG",
    layout="wide"
)

st.title(
    "Enterprise RAG Assistant"
)

st.write(
    "Ask questions from the enterprise policy document."
)

department = st.selectbox(
    "Select Department",
    [
        "hr",
        "security",
        "it"
    ]
)

question = st.text_input( "Enter your question")

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question." )
    else:
        with st.spinner("Searching..."):
            try:
                response = requests.post(
                    f"{FASTAPI_URL}/ask",

                    json={
                        "question":
                            question,

                        "department":
                            department
                    },

                    timeout=180
                )


                if response.status_code == 200:

                    data = (response.json())
                    st.subheader("Answer")
                    st.write(data["answer"])
                    st.write("**Confidence:**",data["confidence"])
                    if data["sources"]:
                        st.subheader( "Sources")
                        for source in (data["sources"]):
                            st.write(
                                f"""
**File:** {source['file']}  
**Page:** {source['page']}  
**Department:** {source['department']}  
**Chunk ID:** {source['chunk_id']}  
**Rerank Score:** {source['rerank_score']:.4f}
""" )
                else:
                    st.error(
                        f"FastAPI error: {response.status_code}"
                    )

            except requests.RequestException as error:
                st.error(
                    f"Backend connection failed: {error}"
                )