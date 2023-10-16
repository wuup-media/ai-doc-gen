from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import os

# Initialize ChromaDB
chroma_client = PersistentClient(path="db")
embedder = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"])
collection = chroma_client.get_or_create_collection(
    name="code", embedding_function=embedder)


def query_collection(sentences):
    return collection.query(
        query_texts=[sent.text for sent in sentences],
        n_results=5
    )
