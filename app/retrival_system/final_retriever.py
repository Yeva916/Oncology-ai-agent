from app.retrival_system.keyword_retriever import keyword_retriever
from app.retrival_system.vector_retriever import vector_retriever
from app.retrival_system.hybrid_retriever import hybrid_retriever
from app.db.vector_db.client import VectorClient
def final_retriever(user_query, alpha=0.5):
    """
    Executes both keyword and vector retrieval, then combines results using a hybrid approach.
    """
    # vector_client = VectorClient()  # Initialize the vector client
    print("keyword_retriever is being called")
    keyword_results = keyword_retriever(user_query)
    print("keyword_retriever results:", len(keyword_results))
    print("vector_retriever is being called")
    vector_results = vector_retriever(user_query)
    print("vector_retriever results:", len(vector_results))
    print("hybrid_retriever is being called")
    combined_results = hybrid_retriever(keyword_results, vector_results, alpha)
    print("hybrid_retriever results:", len(combined_results))
    return combined_results