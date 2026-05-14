from app.retrival_system.keyword_retriever import keyword_retriever
from app.retrival_system.vector_retriever import vector_retriever
from app.retrival_system.hybrid_retriever import hybrid_retriever
from app.db.vector_db.client import VectorClient
def final_retriever(user_query, alpha=0.5):
    """
    Executes both keyword and vector retrieval, then combines results using a hybrid approach.
    """
    # vector_client = VectorClient()  # Initialize the vector client
    keyword_results = keyword_retriever(user_query)
    vector_results = vector_retriever(user_query)
    
    combined_results = hybrid_retriever(keyword_results, vector_results, alpha)
    
    return combined_results