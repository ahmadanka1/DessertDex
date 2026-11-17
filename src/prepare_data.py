import ast
import json
import pandas as pd

SRC = "data/dataset.csv"
OUT = "data/desserts.jsonl"
SAMPLE_SIZE = 3000
SEED = 42


def parse_list(value):
    """Turn a string like "['a', 'b']" into a real list. Bad values become []."""
    if pd.isna(value):
        return []
    try:
        parsed = ast.literal_eval(value)
        return parsed if isinstance(parsed, list) else []
    except (ValueError, SyntaxError):
        return []


def to_int_or_none(value):
    value = pd.to_numeric(value, errors="coerce")
    return None if pd.isna(value) else int(value)


def main():
    df = pd.read_csv(
    SRC,
    sep=";",
    encoding="cp1252",
    encoding_errors="replace",
    on_bad_lines="warn",
    )
    print("Loaded:", df.shape)

    # 1. Keep desserts only
    df = df[df["Category"].str.contains("Dessert", case=False, na=False)].copy()
    print("Desserts:", len(df))

    before = len(df)
    df = df.drop_duplicates(subset="URL")
    print(f"Removed {before - len(df)} duplicate recipes")

    # 2. Convert list-like text columns into real lists
    for col in ["Category", "Cuisine", "Ingredients_Raw", "Instructions"]:
        df[col] = df[col].apply(parse_list)

    # 3. Drop recipes with no ingredients or steps, and ones with few ratings
    df = df[(df["Ingredients_Raw"].str.len() > 0) & (df["Instructions"].str.len() > 0)]
    df = df[df["Rating Count"].fillna(0) >= 10]
    print("After cleaning:", len(df))

    # 4. Sample a manageable number
    if len(df) > SAMPLE_SIZE:
        df = df.sample(SAMPLE_SIZE, random_state=SEED)

    # 5. Save one JSON object per line
    with open(OUT, "w", encoding="utf-8") as f:
        for i, row in enumerate(df.to_dict("records")):
            record = {
                "id": i,
                "name": row["Name"],
                "categories": row["Category"],
                "cuisine": row["Cuisine"],
                "rating": row["Rating Value"] if pd.notna(row["Rating Value"]) else None,
                "rating_count": to_int_or_none(row["Rating Count"]),
                "prep_minutes": to_int_or_none(row["Preparation Time"]),
                "cook_minutes": to_int_or_none(row["Cooking Time"]),
                "ingredients": row["Ingredients_Raw"],
                "instructions": row["Instructions"],
                "url": row["URL"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved {len(df)} recipes to {OUT}")


if __name__ == "__main__":
    main()