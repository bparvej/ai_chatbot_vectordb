import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model for embedding
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FAISS index
dimension = 384  # This matches the embedding dimension of the all-MiniLM-L6-v2 model
index = faiss.IndexFlatL2(dimension)

# Function to read text files from a folder
def load_text_files(folder_path):
    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
                text = file.read()
                documents.append((file_name, text))
    return documents

# Store text embeddings in FAISS
def store_data(folder_path):
    documents = load_text_files(folder_path)
    texts = []
    embeddings = []

    # Process the documents
    for i, (file_name, text) in enumerate(documents):
        # Split text into chunks (e.g., sentences)
        chunks = text.split(".")  # Split by period for simplicity
        for chunk in chunks:
            if chunk.strip():  # Avoid empty chunks
                # Encode the chunk into an embedding
                embedding = embedding_model.encode(chunk)
                embeddings.append(embedding)
                texts.append((chunk, file_name))

    # Convert embeddings list to numpy array
    embeddings = np.array(embeddings).astype("float32")

    # Add the embeddings to the FAISS index
    index.add(embeddings)

    # Save the index for later use
    faiss.write_index(index, "faiss_index.index")

    # Return texts for later querying
    return texts

# Run the storage process
texts = store_data("text_files")  # Change to your folder containing text files
print("Data stored in FAISS index.")

