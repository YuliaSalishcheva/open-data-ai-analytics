import pandas as pd
import requests
import os
from pathlib import Path
from sqlalchemy import create_engine


def load_data():
    base_path = Path(__file__).resolve().parent.parent
    raw_data_dir = base_path / "data" / "raw"
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    file_name = "176-zakladi-zagalnoyi-serednoyi-osviti.xlsx"
    file_path = raw_data_dir / file_name
    url = "https://data.gov.ua/dataset/427229a8-011d-4dc2-b82e-cbee708cbc03/resource/be955d39-d650-4d3c-88c0-8b25c5051df0/download/176-zakladi-zagalnoyi-serednoyi-osviti.xlsx"

    if not file_path.exists():
        print(f"Downloading file...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            print("Download complete.")
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

    try:
        print("Reading Excel file...")
        df = pd.read_excel(file_path, sheet_name=1)
        return df
    except Exception as e:
        print(f"Error reading data: {e}")
        return None


def save_to_postgres(df):
    try:
        # БЕРЕМО URL ПРЯМО З ТВOГО COMPOSE.YAML
        connection_string = os.getenv('DATABASE_URL')

        if not connection_string:
            print("DATABASE_URL not found in environment!")
            return False

        engine = create_engine(connection_string)

        print("Loading data to PostgreSQL (analytics_db)...")
        # Записуємо в таблицю raw_data
        df.to_sql('raw_data', engine, if_exists='replace', index=False)
        print("Successfully loaded to PostgreSQL!")
        return True
    except Exception as e:
        print(f"Error saving to DB: {e}")
        return False


if __name__ == "__main__":
    df = load_data()
    if df is not None:
        print("Preview of data:")
        print(df.head())
        save_to_postgres(df)