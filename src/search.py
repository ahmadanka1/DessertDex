import json
import sys
import faiss
import numpy as np
from fastembed import TextEmbedding

DATA = "data/desserts.jsonl"
INDEX_PATH = "data/index.faiss"


def load():
    with open(DATA, encoding="utf-8") as f:
        recipes = [json.loads(line) for line in f]
    index = faiss.read_index(INDEX_PATH)
    model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    return recipes, index, model


def search(query, recipes, index, model, k=5):
    vec = np.array(list(model.embed([query])), dtype="float32")
    faiss.normalize_L2(vec)
    scores, ids = index.search(vec, k)
    return [(recipes[i], float(score)) for i, score in zip(ids[0], scores[0])]


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "chocolate cake with no eggs"
    recipes, index, model = load()
    for r, score in search(query, recipes, index, model):
        print(f"{score:.3f}  {r['name']}  ({r['url']})")