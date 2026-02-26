import pandas as pd
import json
from pathlib import Path


def load_data():
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "data" / "raw"
    json_files = list(file_path.glob("*.json"))

    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    # Беремо другий елемент (основні дані)
    df = pd.DataFrame(data[1])

    return df


def check_data_quality(df):
    print("\n===== DATA INFO =====")
    print(df.info())

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== DUPLICATES =====")
    print(df.duplicated().sum())


if __name__ == "__main__":
    df = load_data()
    check_data_quality(df)