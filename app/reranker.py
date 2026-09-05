from sentence_transformers import CrossEncoder
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank_results(query,candidate_results,chunks):

    candidate_indices = [idx for idx, score in candidate_results]
    pairs = []

    for idx in candidate_indices:
        pairs.append(
            [
                query,
                chunks[idx]["text"]
            ]
        )

    rerank_scores = (reranker.predict(pairs))

    reranked_results = list(zip(candidate_indices,rerank_scores))

    reranked_results = sorted(reranked_results,key=lambda x: x[1],reverse=True)

    return reranked_results