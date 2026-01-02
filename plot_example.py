import os
import pandas as pd
import matplotlib.pyplot as plt

DATA = os.path.join("data", "sample.csv")
OUT = os.path.join("output", "example.png")

os.makedirs("output", exist_ok=True)

df = pd.read_csv(DATA, parse_dates=[0])
df = df.sort_values(df.columns[0])

plt.figure(figsize=(8, 4))
plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o')
plt.title("Sample plot")
plt.xlabel(df.columns[0])
plt.ylabel(df.columns[1])
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT, dpi=150)
print(f"Wrote {OUT}")
