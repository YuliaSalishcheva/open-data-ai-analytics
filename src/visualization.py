import pandas as pd
import requests
import matplotlib.pyplot as plt
from pathlib import Path
import os

def load_data():
    base_path = Path(__file__).resolve().parent.parent
    raw_data_dir = base_path / "data" / "raw"
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    
    file_name = "176-zakladi-zagalnoyi-serednoyi-osviti.xlsx"
    file_path = raw_data_dir / file_name
    url = "https://data.gov.ua/dataset/427229a8-011d-4dc2-b82e-cbee708cbc03/resource/be955d39-d650-4d3c-88c0-8b25c5051df0/download/176-zakladi-zagalnoyi-serednoyi-osviti.xlsx"

    if not file_path.exists():
        print(f"Downloading data from {url}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            print("Download complete.")
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
    if df is None or df.empty:
        print("DataFrame is empty or None. Visualization skipped.")
        return

    print("\n===== VISUALIZATION =====")
    base_path = Path(__file__).resolve().parent.parent
    output_dir = base_path / "artifacts" / "visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    actual_columns = df.columns.tolist()
    print(f"Real columns found in dataset: {actual_columns}")

    try:
        plt.style.use("seaborn-v0_8")
    except:
        plt.style.use("ggplot")

    time_col = next((c for c in actual_columns if c.lower() in ['period', 'період', 'рік', 'year']), None)
    
    if time_col:
        plt.figure(figsize=(10, 6))
        yearly_counts = df[time_col].value_counts().sort_index()
        plt.plot(yearly_counts.index.astype(str), yearly_counts.values, marker="o", color='teal')
        plt.title(f"Records Distribution by {time_col}", fontsize=14)
        plt.grid(True)
        
        save_path = output_dir / "time_distribution.png"
        plt.savefig(save_path)
        print(f"Chart saved to: {save_path}")
    else:
        print("Time-related column not found — skipping line chart.")

    try:
        plt.figure(figsize=(10, 6))
        target_col = actual_columns[1] if len(actual_columns) > 1 else actual_columns[0]
        df[target_col].value_counts().head(10).plot(kind="barh", color='skyblue')
        plt.title(f"Top 10 Distribution: {target_col}", fontsize=14)
        plt.tight_layout()
        
        save_path = output_dir / "top10_distribution.png"
        plt.savefig(save_path)
        print(f"Chart saved to: {save_path}")
    except Exception as e:
        print(f"Error drawing bar chart: {e}")

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg') 
    
    df = load_data()
    visualize_data(df)