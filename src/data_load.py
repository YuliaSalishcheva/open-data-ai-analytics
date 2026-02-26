import pandas as pd
from pathlib import Path


def load_data():
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "data" / "raw"

    json_files = list(file_path.glob("*.json"))

    if not json_files:
        print("No JSON files found in data/raw")
        return

    file_to_load = json_files[0]

    try:
        df = pd.read_json(file_to_load)
        print(f"Loaded file: {file_to_load.name}")
        print(df.head())
        return df
    except Exception as e:
        print("Error loading data:", e)


if __name__ == "__main__":
    load_data()