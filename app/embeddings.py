import numpy as np
from sentence_transformers import SentenceTransformer 

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(texts):
    embeddings = embedding_model.encode(texts)
    embeddings = np.array(embeddings,dtype="float32")
    return embeddings

def create_query_embedding(query):
    embedding = embedding_model.encode( [query])
    embedding = np.array(
        embedding,
        dtype="float32"
    )
    return embedding