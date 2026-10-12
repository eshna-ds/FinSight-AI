
from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "processed" / "financial_features.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "anomaly_results.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    features = [
        "revenue",
        "net_profit",
        "total_debt",
        "operating_cash_flow",
        "revenue_growth_pct",
        "receivables_growth_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "cash_flow_to_profit",
        "receivables_vs_revenue_growth_pp",
    ]

    missing_columns = set(features) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing feature columns: {sorted(missing_columns)}"
        )

    # Replace infinite values with missing values.
    df[features] = df[features].replace(
        [float("inf"), float("-inf")], float("nan")
    )

    # Remove features that have no usable values.
    usable_features = [
        column for column in features
        if df[column].notna().any()
    ]

    if len(df) < 3:
        raise ValueError("At least 3 records are required.")

    if not usable_features:
        raise ValueError("No usable financial features found.")

    # Fill missing values, scale features, and detect anomalies.
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        IsolationForest(
            n_estimators=100,
            contamination="auto",
            random_state=42,
        ),
    )

    X = df[usable_features]
    predictions = model.fit_predict(X)
    scores = model.decision_function(X)

    df["anomaly_label"] = predictions
    df["anomaly_status"] = df["anomaly_label"].map({
        -1: "Potential anomaly",
        1: "Not flagged",
    })
    df["anomaly_score"] = scores

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(
        df[
            [
                "company",
                "year",
                "anomaly_status",
                "anomaly_score",
            ]
        ].sort_values("anomaly_score").to_string(index=False)
    )

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
