import os
import pandas as pd
from sqlalchemy import create_engine


def load_from_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set")

    engine = create_engine(db_url)

    df = pd.read_sql("SELECT * FROM raw_data", engine)
    return df


def research(df):
    print("\n===== BASIC STATISTICS =====")
    print(df.describe(include="all"))

    # приклад агрегацій
    if "code" in df.columns:
        df["code"] = df["code"].astype(str)

        schools = df[df["code"] == "01"]
        students = df[df["code"] == "02"]

        result = pd.DataFrame({
            "total_schools": [schools["data"].sum()],
            "total_students": [students["data"].sum()],
        })

        print("\n===== SUMMARY =====")
        print(result)

        return result

    return None


def save_results(result):
    if result is None:
        return

    os.makedirs("/shared", exist_ok=True)
    result.to_csv("/shared/research_results.csv", index=False)

    print("Research results saved to /shared")


if __name__ == "__main__":
    df = load_from_db()
    result = research(df)
    save_results(result)