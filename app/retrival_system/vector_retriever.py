from app.db.vector_db.client import VectorClient

def vector_retriever(search_query):
    vector_store = VectorClient()
    docs = vector_store.get_vector_store().similarity_search_with_score(search_query, k=5)
    # docs = retriever.similarity_search_with_score(search_query, k=5)
    output = []
    for doc, score in docs:
        output.append({
            "nct_id": doc.metadata.get("nct_id", "unknown"),
            "score": score,
            # "content": doc.page_content
        })

    return output

print(vector_retriever("non small lung cancer Osimertinib age above 18"))
#[{'nct_id': 'NCT06670196', 'score': 0.694561839}, {'nct_id': 'NCT06417814', 'score': 0.689498901}]