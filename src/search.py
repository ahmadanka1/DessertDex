import json
import sys
import faiss
from sentence_transformers import SentenceTransformer

DATA = "data/desserts.jsonl"
INDEX_PATH = "data/index.faiss"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load():
    with open(DATA, encoding="utf-8") as f:
        recipes = [json.loads(line) for line in f]
    index = faiss.read_index(INDEX_PATH)
    model = SentenceTransformer(MODEL_NAME)
    return recipes, index, model


def search(query, recipes, index, model, k=5):
    vec = model.encode([query], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(vec, k)
    return [(recipes[i], float(s)) for i, s in zip(ids[0], scores[0])]


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "chocolate cake with no eggs"
    recipes, index, model = load()
    for r, score in search(query, recipes, index, model):
        print(f"{score:.3f}  {r['name']}  ({r['url']})")