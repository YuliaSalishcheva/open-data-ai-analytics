import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from pathlib import Path


def load_from_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set")

    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM raw_data", engine)
    return df


def visualize(df):
    if df is None or df.empty:
        print("No data in database")
        return

    output_dir = Path("/app/artifacts/visualization")
    output_dir.mkdir(parents=True, exist_ok=True)

    # беремо першу текстову колонку (без “магії” типу 01/02)
    text_cols = df.select_dtypes(include="object").columns

    if len(text_cols) == 0:
        print("No categorical columns found")
        return

    col = text_cols[0]

    plt.figure(figsize=(12, 6))

    df[col].value_counts().head(15).sort_values().plot(kind="barh")

    plt.title(f"Top values in {col}")
    plt.tight_layout()

    output_file = output_dir / "chart.png"
    plt.savefig(output_file)

    print(f"Saved visualization to {output_file}")


if __name__ == "__main__":
    df = load_from_db()
    visualize(df)