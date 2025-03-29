import os
import chromadb
import spacy
from sentence_transformers import SentenceTransformer

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("knowledge_base")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to read text files from a folder
def load_text_files(folder_path):
    documents = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
                text = file.read()
                documents.append((file_name, text))
    return documents

# Function to split text into sentences
def split_into_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

# Store text embeddings in ChromaDB
def store_data(folder_path):
    documents = load_text_files(folder_path)
    for i, (file_name, text) in enumerate(documents):
        sentences = split_into_sentences(text)
        for j, sentence in enumerate(sentences):
            embedding = embedding_model.encode(sentence).tolist()
            collection.add(
                ids=[f"{i}_{j}"],  # Unique ID for each sentence
                embeddings=[embedding],
                metadatas=[{"text": sentence, "file": file_name}]
            )
    print(f"Stored {sum(len(split_into_sentences(text)) for _, text in documents)} sentences in ChromaDB.")

# Run the storage process
store_data("text_files")  # Change to your folder containing text files
