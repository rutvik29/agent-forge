"""Memory management for agents."""
import chromadb
from chromadb.utils import embedding_functions
from typing import List
import hashlib, time

class LongTermMemory:
    def __init__(self, collection="agent_memory", host="localhost", port=8002):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-3-small")
        self.collection = self.client.get_or_create_collection(collection, embedding_function=self.ef)

    def store(self, content: str, metadata: dict = None) -> str:
        doc_id = hashlib.md5(f"{content}{time.time()}".encode()).hexdigest()
        self.collection.add(documents=[content], metadatas=[metadata or {}], ids=[doc_id])
        return doc_id

    def retrieve(self, query: str, n_results: int = 5) -> List[str]:
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results["documents"][0] if results["documents"] else []
