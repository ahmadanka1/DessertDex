import json

from search import load, search
from generate import MIN_SCORE

K = 5


def is_relevant(recipe, terms):
    text = (recipe["name"] + " " + " ".join(recipe["ingredients"])).lower()
    return all(t in text for t in terms)


def main():
    with open("eval_set.json", encoding="utf-8") as f:
        tests = json.load(f)

    recipes, index, model = load()
    precisions, top1_hits, refusal_passes = [], [], []

    for t in tests:
        hits = search(t["query"], recipes, index, model, k=K)
        best_score = hits[0][1]

        if t.get("expect_none"):
            ok = best_score < MIN_SCORE
            refusal_passes.append(ok)
            print(f"[{'PASS' if ok else 'FAIL'}] (should refuse) {t['query']!r}  best score {best_score:.2f}")
        else:
            rel = [is_relevant(r, t["expect_all"]) for r, _ in hits]
            precisions.append(sum(rel) / K)
            top1_hits.append(rel[0])
            print(f"[{sum(rel)}/{K}] {t['query']!r}  top1={'yes' if rel[0] else 'no'}  best score {best_score:.2f}")

    print("\n--- Summary ---")
    if precisions:
        print(f"Precision@{K}: {sum(precisions) / len(precisions):.2f}")
        print(f"Top-1 relevant: {sum(top1_hits)}/{len(top1_hits)}")
    if refusal_passes:
        print(f"Correct refusals: {sum(refusal_passes)}/{len(refusal_passes)}")


if __name__ == "__main__":
    main()