
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "processed" / "financial_data.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "anomaly_results.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    features = [
        "revenue",
        "net_profit",
        "total_debt",
        "receivables",
        "operating_cash_flow",
        "total_equity",
    ]

    # Check whether required financial values are missing
    if df[features].isna().any().any():
        raise ValueError("Missing financial values in the dataset.")

    if len(df) < 3:
        raise ValueError("At least 3 records are required.")

    # Standardize the financial values
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    # Train the anomaly detection model
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42,
    )

    predictions = model.fit_predict(X)

    df["anomaly_label"] = predictions
    df["anomaly_status"] = df["anomaly_label"].map({
        -1: "Potential anomaly",
        1: "Not flagged",
    })

    df["anomaly_score"] = model.decision_function(X)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(df[
        ["company", "year", "anomaly_status", "anomaly_score"]
    ].to_string(index=False))

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

