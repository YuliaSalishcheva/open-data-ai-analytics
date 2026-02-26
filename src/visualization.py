import os
import json
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(
        base_dir,
        "data",
        "raw",
        "176-zakladi-zagalnoyi-serednoyi-osviti.json"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "data" in raw:
        df = pd.DataFrame(raw["data"])
    else:
        df = pd.DataFrame(raw)

    return df


def visualize_data(df):
    print("\n===== VISUALIZATION =====")

    plt.style.use("seaborn-v0_8")

    if "period" in df.columns:
        yearly_counts = df["period"].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        plt.plot(yearly_counts.index, yearly_counts.values, marker="o")
        plt.title("Dynamics of School Records by Year", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Number of Records", fontsize=12)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("Column 'period' not found — skipping year chart.")

    if "code" in df.columns:
        code_counts = df["code"].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        code_counts.sort_values().plot(kind="barh")
        plt.title("Top 10 Codes Distribution", fontsize=14)
        plt.xlabel("Count", fontsize=12)
        plt.ylabel("Code", fontsize=12)
        plt.tight_layout()
        plt.show()
    else:
        print("Column 'code' not found — skipping code chart.")


if __name__ == "__main__":
    df = load_data()
    visualize_data(df)