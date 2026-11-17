with open("data/dataset.csv", "r", encoding="utf-8", errors="replace", newline="") as f:
    for i in range(4):
        line = f.readline()
        print(f"--- line {i+1} ({len(line)} chars) ---")
        print(line[:600])