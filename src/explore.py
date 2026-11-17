import pandas as pd

SRC = "data/dataset.csv"
df = pd.read_csv(
    SRC,
    sep=";",
    encoding="cp1252",
    encoding_errors="replace",
    on_bad_lines="warn",
    )
print(df.shape)                 # expect about 50,510 rows and 18 columns
print(df.columns.tolist())
print(df["Category"].head(10))
print(df.isna().sum())          # missing values per column