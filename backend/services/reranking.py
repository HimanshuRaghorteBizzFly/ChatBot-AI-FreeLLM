"""
Reranking service.
Scores and ranks a set of candidate documents against a search query.
"""
from typing import List, Dict, Any
from backend.services.embeddings import generate_text_embedding, cosine_similarity
from backend.repositories.storage import log_usage

def rerank_documents(query: str, documents: List[str], model: str = "cross-encoder-rerank-v1") -> List[Dict[str, Any]]:
    """
    Computes semantic relevance ranking for candidate documents relative to a query.
    """
    if not query.strip() or not documents:
        return []

    # Generate query embedding
    q_res = generate_text_embedding(query)
    q_vec = q_res.get("vector", [])

    results = []
    for idx, doc in enumerate(documents):
        if not doc.strip():
            continue
        d_res = generate_text_embedding(doc)
        d_vec = d_res.get("vector", [])
        
        # Calculate score
        if q_vec and d_vec:
            score = cosine_similarity(q_vec, d_vec)
        else:
            # Word-overlap heuristic fallback
            q_words = set(query.lower().split())
            d_words = set(doc.lower().split())
            score = len(q_words & d_words) / max(len(q_words), 1)

        results.append({
            "original_index": idx + 1,
            "document": doc.strip(),
            "score": round(max(0.0, min(1.0, score)), 4)
        })

    # Sort descending by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    for rank, item in enumerate(results, start=1):
        item["rank"] = rank

    log_usage("AI Studio", model, "reranking", input_tokens=len(query.split()) + sum(len(d.split()) for d in documents))
    return results
