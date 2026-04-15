from app.db.vector_db.client import VectorClient

def vector_retriever(search_query):
    vector_store = VectorClient()
    retriever = vector_store.get_vector_store().as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke(search_query)
    output = []
    for doc in docs:
        output.append({
            "nct_id": doc.metadata.get("nct_id", "unknown"),
            # "content": doc.page_content
        })

    return output

print(vector_retriever("non small lung cancer Osimertinib age above 18"))