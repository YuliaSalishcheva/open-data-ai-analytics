import pandas as pd
import json
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def load_data():
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "data" / "raw"
    json_files = list(file_path.glob("*.json"))

    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data[1])
    df["data"] = pd.to_numeric(df["data"], errors="coerce")
    return df


def research(df):

    schools = df[df["code"] == "01"].copy().sort_values("period")
    students = df[df["code"] == "02"].copy().sort_values("period")


    plt.figure(figsize=(10, 5))
    plt.plot(schools["period"], schools["data"])
    plt.xticks(rotation=45)
    plt.title("Number of Schools Over Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Schools")
    plt.tight_layout()
    plt.show()


    plt.figure(figsize=(10, 5))
    plt.plot(students["period"], students["data"])
    plt.xticks(rotation=45)
    plt.title("Number of Students Over Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()


    merged = pd.merge(
        schools[["period", "data"]],
        students[["period", "data"]],
        on="period",
        suffixes=("_schools", "_students"),
    )

    merged["students_per_school"] = (
        merged["data_students"] / merged["data_schools"]
    )

    plt.figure(figsize=(10, 5))
    plt.plot(merged["period"], merged["students_per_school"])
    plt.xticks(rotation=45)
    plt.title("Average Students per School")
    plt.xlabel("Year")
    plt.ylabel("Students per School")
    plt.tight_layout()
    plt.show()

    schools["year_numeric"] = schools["period"].str[:4].astype(int)

    X = schools[["year_numeric"]]
    y = schools["data"]

    model = LinearRegression()
    model.fit(X, y)

    predictions_train = model.predict(X)
    r2 = r2_score(y, predictions_train)

    print("\n===== MODEL EVALUATION =====")
    print(f"R² score: {r2:.4f}")
    print(f"Intercept: {model.intercept_:.2f}")

    future_years = pd.DataFrame({"year_numeric": [2025, 2026, 2027]})
    predictions = model.predict(future_years)

    print("\n===== MODEL PREDICTION =====")
    for year, pred in zip(future_years["year_numeric"], predictions):
        print(f"Predicted number of schools in {year}: {int(pred)}")


if __name__ == "__main__":
    df = load_data()
    research(df)