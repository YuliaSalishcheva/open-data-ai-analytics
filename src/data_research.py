import pandas as pd
import requests
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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
        df = pd.read_excel(file_path, sheet_name=1) 
        
        if "data" in df.columns:
            df["data"] = pd.to_numeric(df["data"], errors="coerce")
        return df
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def research(df):
    if df is None:
        return

    if "code" in df.columns:
        df["code"] = df["code"].astype(str).str.zfill(2)

    schools = df[df["code"] == "01"].copy().sort_values("period")
    students = df[df["code"] == "02"].copy().sort_values("period")

    plt.figure(figsize=(10, 5))
    plt.plot(schools["period"].astype(str), schools["data"])
    plt.xticks(rotation=45)
    plt.title("Number of Schools Over Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Schools")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(students["period"].astype(str), students["data"])
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
    plt.plot(merged["period"].astype(str), merged["students_per_school"])
    plt.xticks(rotation=45)
    plt.title("Average Students per School")
    plt.xlabel("Year")
    plt.ylabel("Students per School")
    plt.tight_layout()
    plt.show()

    schools["year_numeric"] = schools["period"].astype(str).str[:4].astype(int)
    schools = schools.dropna(subset=["data", "year_numeric"])

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