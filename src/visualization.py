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
        try:
            response = requests.get(url, timeout=30)
            with open(file_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error: {e}")
            return None

    try:
        df = pd.read_excel(file_path, sheet_name=1) 
        return df
    except:
        return pd.read_excel(file_path)

def visualize_data(df):
    if df is None or df.empty:
        return

    print("\n===== ГЕНЕРАЦІЯ РЕАЛЬНОЇ АНАЛІТИКИ =====")
    output_dir = Path(__file__).resolve().parent.parent / "artifacts" / "visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    actual_columns = df.columns.tolist()
    target_col = next((c for c in actual_columns if any(word in str(c).lower() for word in ['область', 'region', 'територія', 'назва'])), actual_columns[min(2, len(actual_columns)-1)])

    plt.figure(figsize=(12, 8))
    
    counts = df[target_col].value_counts().head(15)
    
    counts.sort_values().plot(kind='barh', color='salmon', edgecolor='black')
    
    plt.title(f"ТОП-15 за категорією: {target_col}", fontsize=14)
    plt.xlabel("Кількість закладів (частота)", fontsize=12)
    plt.ylabel("Найменування", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    plt.savefig(output_dir / "real_data_chart.png")
    print(f"Готово! Графік 'real_data_chart.png' створено на основі колонки '{target_col}'")

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg') 
    df = load_data()
    visualize_data(df)