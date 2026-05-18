from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Read text file containing the policy document.
# Each line is treated as a separate document chunk in this simple example.
file_path = "data/policy.txt"

with open(file_path, "r", encoding="utf-8") as file:
    docs = file.readlines()

# Strip whitespace and ignore empty lines.
docs = [doc.strip() for doc in docs if doc.strip()]

print("Documents:")
print(docs)

# Load the sentence transformer model for embedding creation.
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for each document chunk.
doc_vectors = model.encode(docs)

# Convert embeddings to float32, which FAISS requires.
doc_vectors = np.array(doc_vectors).astype("float32")

# Create a simple FAISS index using L2 distance.
dimension = doc_vectors.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add the document vectors into the index.
index.add(doc_vectors)

# Define the user query to search against the documents.
# This query is encoded and compared with stored document vectors.
question = "what is Office hours?"

# Create query embedding
q_vector = model.encode([question])
q_vector = np.array(q_vector).astype("float32")

# Search similar document
distance, ids = index.search(q_vector, k=1)

# Retrieve best match
context = docs[ids[0][0]]

print("\nQuestion:", question)
print("Retrieved:", context)