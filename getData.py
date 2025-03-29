import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("knowledge_base")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# User Query
query = "When DSE start trading?"

# Generate embedding for query
query_embedding = embedding_model.encode(query).tolist()

# Search in ChromaDB (increase results for better accuracy)
results = collection.query(query_embeddings=[query_embedding], n_results=3)

# Process Results
if results["ids"]:
    best_match = results["metadatas"][0][0]["text"]  # Top result
    response = best_match
else:
    response = "I don't know."

print("Response:", response)
