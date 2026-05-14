from app.db.vector_db.client import VectorClient


def vector_retriever(search_query, limit=5):
    """Return vector-ranked clinical trials for a search query."""
    vector_store = VectorClient()
    docs = vector_store.get_vector_store().similarity_search_with_score(search_query, k=limit)

    output = []
    for doc, score in docs:
        output.append({
            "nct_id": doc.metadata.get("nct_id", "unknown"),
            "score": score,
        })
    # print(f"Vector Retriever Output for query '{search_query}': {output}")
    return output