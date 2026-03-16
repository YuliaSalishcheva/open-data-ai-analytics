import pandas as pd
import requests
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

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        print(df.head())