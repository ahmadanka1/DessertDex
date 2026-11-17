import os
import requests

URL = "https://zenodo.org/records/15169428/files/dataset.csv?download=1"
OUT = os.path.join("data", "dataset.csv")

def main():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(OUT):
        print("Already downloaded.")
        return
    print("Downloading (110 MB)...")
    with requests.get(URL, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(OUT, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
    print("Done:", OUT)

if __name__ == "__main__":
    main()