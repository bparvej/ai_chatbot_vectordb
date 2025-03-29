import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model for embedding
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the FAISS index
index = faiss.read_index("faiss_index.index")

# Function to get the embedding for the user query
def query_faiss(query):
    # Generate the embedding for the query
    query_embedding = embedding_model.encode(query).astype("float32").reshape(1, -1)
    
    # Search the FAISS index
    k = 1  # Number of nearest neighbors to return
    D, I = index.search(query_embedding, k)

    # Fetch the most similar document
    if I[0][0] != -1:  # If a match is found
        # Retrieve the matched document and the corresponding text
        result_text = texts[I[0][0]][0]
        return result_text
    else:
        return "I don't know."

# User query
query = "When the formal trading of DSE started and where?"

# Query FAISS for the most relevant chunk
response = query_faiss(query)
print("Response:", response)
