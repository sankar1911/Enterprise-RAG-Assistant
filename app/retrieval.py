import faiss


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def hybrid_search(query,query_embedding,chunks,index, k=10):
    k = min( k,len(chunks))

    distances, indices = index.search(
        query_embedding,
        k=k
    )

    scores = {}

    for i, idx in enumerate(indices[0]):
        distance = float(distances[0][i])
        semantic_score = ( 1 / (1 + distance))
        scores[int(idx)] = (semantic_score)
    query_words = (query.lower().split())

    for idx, chunk in enumerate(chunks):

        text = (chunk["text"].lower())
        keyword_score = 0
        for word in query_words:
            if word in text:
                keyword_score += 1
        if keyword_score > 0:
            if idx not in scores:
                scores[idx] = 0
            scores[idx] += (
                keyword_score
            )

    ranked_results = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_results