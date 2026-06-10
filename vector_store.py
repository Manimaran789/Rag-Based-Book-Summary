import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load once
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Global storage
chunks_store = []
index = None


def store_chunks(chunks):
    global chunks_store, index

    if not chunks:
        print("❌ No chunks received")
        return

    chunks_store = chunks

    embeddings = embed_model.encode(
    chunks,
    batch_size=32,
    show_progress_bar=True
)
    embeddings = np.array(embeddings).astype("float32")

    # 🔥 Normalize (CRITICAL)
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity

    index.add(embeddings)

    print("✅ Stored chunks:", len(chunks))
    print("✅ Index size:", index.ntotal)


def retrieve(query, top_k=3):
    global index, chunks_store

    if index is None or index.ntotal == 0:
        print("❌ Retrieval failed: index empty")
        return []

    if not query.strip():
        print("❌ Empty query")
        return []

    query_vec = embed_model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    # 🔥 Normalize query
    faiss.normalize_L2(query_vec)

    distances, indices = index.search(query_vec, top_k)

    print("🔍 Query:", query)
    print("📊 Scores:", distances)
    print("📄 Indices:", indices)

    results = []
    for i in indices[0]:
        if 0 <= i < len(chunks_store):
            results.append(chunks_store[i])

    print("✅ Retrieved chunks:", len(results))
    return results