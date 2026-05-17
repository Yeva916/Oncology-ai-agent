
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from app.config import settings

class VectorClient:
    def __init__(self,):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        
        self.index_name = "oncology"
        self.embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",output_dimensionality=1024)

 
        self.index = self.pc.Index(self.index_name)

        self.vector_client = PineconeVectorStore(embedding=self.embeddings,
                                                index=self.index,
                                                )

    def get_vector_store(self,):
            return self.vector_client
    
    def add_documents(self,docs):
        self.vector_client.add_documents(docs)