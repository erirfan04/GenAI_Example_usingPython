from sentence_transformers import SentenceTransformer
import faiss

docs = [
    "Employees get 20 paid leaves per year",
    "WFH allowed twice a week"
]

model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
doc_vectors = model.encode(docs)

# Store in FAISS(Facebook AI Similarity Search)
# 384 means: The dimension (size) of the embedding vectors.
index = faiss.IndexFlatL2(384)
index.add(doc_vectors)

# User query
question = "How many leaves do we get?"
q_vector = model.encode([question])

# Search
_, ids = index.search(q_vector, k=1)

context = docs[ids[0][0]]

print("Retrieved:", context)