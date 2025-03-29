from flask import Flask, render_template, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer

app = Flask(__name__, static_folder="static")


# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("knowledge_base")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"response": "Please enter a question."})

    # Generate embedding for query
    query_embedding = embedding_model.encode(user_query).tolist()

    # Search in ChromaDB
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    if results["ids"]:
        response = results["metadatas"][0][0]["text"]  # Get best match
    else:
        response = "I don't know."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
