import os
import glob
from loader import load_file
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DATA_FOLDER = "data"

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Supported file types
supported = ["*.csv", "*.txt", "*.md", "*.pdf", "*.docx", "*.html", "*.htm", "*.eml"]

# Load and chunk all files
texts = []

for pattern in supported:
    for file in glob.glob(os.path.join(DATA_FOLDER, pattern)):
        content = load_file(file)
        if not content:
            continue
        # Split into paragraphs for better embeddings
        for para in content.split("\n\n"):
            if para.strip():
                texts.append(f"[{os.path.basename(file)}] {para.strip()}")

# Create embeddings
embeddings = np.array([model.encode(t) for t in texts])
if embeddings.ndim == 1:
    embeddings = embeddings.reshape(1, -1)

def invoke(query: str, k=5):
    query_vec = model.encode([query])
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)
    sims = cosine_similarity(query_vec, embeddings)[0]
    top_k = sims.argsort()[-k:][::-1]
    return "\n".join([texts[i] for i in top_k])
