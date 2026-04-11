
class Retriever:
    def __init__(self,vector_client):
        self.vector_client = vector_client
    
    def retrieve(self,query,k=5):
        vector_store = self.vector_client.get_vector_store()
        docs = vector_store.similarity_search(query,k=k)
        return docs