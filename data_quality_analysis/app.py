import pandas as pd
from sqlalchemy import create_engine
import os


def load_data_from_db():
    connection_string = os.getenv("DATABASE_URL")

    if not connection_string:
        raise ValueError("DATABASE_URL not set")

    engine = create_engine(connection_string)

    query = "SELECT * FROM raw_data"
    df = pd.read_sql(query, engine)

    return df


def check_data_quality(df):
    print("\n===== DATA INFO =====")
    print(df.info())

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== DUPLICATES =====")
    print(df.duplicated().sum())


def save_quality_report(df):
    report = {
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "rows": len(df)
    }

    report_df = pd.DataFrame([report])

    output_path = "/app/reports/quality_report.csv"
    report_df.to_csv(output_path, index=False)

    print(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    df = load_data_from_db()

    check_data_quality(df)
    save_quality_report(df)