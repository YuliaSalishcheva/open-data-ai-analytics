import pandas as pd
import requests
import matplotlib.pyplot as plt
from pathlib import Path

def load_data():
    base_path = Path(__file__).resolve().parent.parent
    raw_data_dir = base_path / "data" / "raw"
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    file_name = "176-zakladi-zagalnoyi-serednoyi-osviti.xlsx"
    file_path = raw_data_dir / file_name
    url = "https://data.gov.ua/dataset/427229a8-011d-4dc2-b82e-cbee708cbc03/resource/be955d39-d650-4d3c-88c0-8b25c5051df0/download/176-zakladi-zagalnoyi-serednoyi-osviti.xlsx"

    if not file_path.exists():
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def visualize_data(df):
    if df is None:
        return

    print("\n===== VISUALIZATION =====")

    try:
        plt.style.use("seaborn-v0_8")
    except:
        plt.style.use("seaborn")

    if "period" in df.columns:
        yearly_counts = df["period"].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        plt.plot(yearly_counts.index.astype(str), yearly_counts.values, marker="o")
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