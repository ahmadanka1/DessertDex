import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DATA = "data/desserts.jsonl"
INDEX_OUT = "data/index.faiss"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_recipes():
    with open(DATA, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def embedding_text(r):
    parts = [f"Dessert: {r['name']}."]
    if r["cuisine"]:
        parts.append("Cuisine: " + ", ".join(r["cuisine"]) + ".")
    parts.append("Ingredients: " + "; ".join(r["ingredients"]))
    return " ".join(parts)


def main():
    recipes = load_recipes()
    texts = [embedding_text(r) for r in recipes]
    print(f"Embedding {len(texts)} recipes...")

    model = SentenceTransformer(MODEL_NAME)
    vectors = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        normalize_embeddings=True,
    ).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])  # inner product = cosine on normalized vectors
    index.add(vectors)
    faiss.write_index(index, INDEX_OUT)
    print(f"Saved index with {index.ntotal} vectors to {INDEX_OUT}")


if __name__ == "__main__":
    main()