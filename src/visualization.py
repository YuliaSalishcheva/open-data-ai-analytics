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
        print(f"Завантаження даних з {url}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            print("Файл успішно завантажено.")
        except Exception as e:
            print(f"Помилка завантаження: {e}")
            return None

    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Помилка читання Excel: {e}")
        return None

def visualize_data(df):
    if df is None or df.empty:
        print("Дані відсутні. Візуалізація скасована.")
        return

    print("\n===== ГЕНЕРАЦІЯ АНАЛІТИКИ =====")
    
    base_path = Path(__file__).resolve().parent.parent
    output_dir = base_path / "artifacts" / "visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams['font.family'] = 'sans-serif'
    try:
        plt.style.use("ggplot")
    except:
        pass
    
    actual_columns = df.columns.tolist()
    print(f"Доступні колонки: {actual_columns}")


    target_col = next((c for c in actual_columns if any(word in c.lower() for word in ['область', 'регіон', 'територія', 'назва', 'тип'])), actual_columns[0])

    try:
        plt.figure(figsize=(12, 8))
        
        counts = df[target_col].value_counts().head(15)
        
        counts.sort_values().plot(kind='barh', color='skyblue', edgecolor='black')
        
        plt.title(f"Розподіл закладів освіти за полем: {target_col}", fontsize=14)
        plt.xlabel("Кількість", fontsize=12)
        plt.ylabel("Значення", fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        save_path = output_dir / "analytics_distribution.png"
        plt.savefig(save_path)
        print(f"Успіх! Графік збережено: {save_path}")
    except Exception as e:
        print(f"Помилка при створенні графіка: {e}")

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg') 
    
    df = load_data()
    visualize_data(df)