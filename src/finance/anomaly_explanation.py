
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "processed" / "anomaly_results.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "investigation_results.csv"


def explain_record(row):
    reasons = []

    if (
        pd.notna(row.get("receivables_vs_revenue_growth_pp"))
        and row["receivables_vs_revenue_growth_pp"] > 20
    ):
        reasons.append(
            "Receivables growth exceeds revenue growth "
            "by more than 20 percentage points"
        )

    if (
        pd.notna(row.get("cash_flow_to_profit"))
        and row["cash_flow_to_profit"] < 0.5
        and row["net_profit"] > 0
    ):
        reasons.append(
            "Operating cash flow is low relative to net profit"
        )

    if (
        pd.notna(row.get("debt_to_equity"))
        and row["debt_to_equity"] > 1
    ):
        reasons.append(
            "Debt exceeds shareholders' equity"
        )

    if not reasons:
        reasons.append(
            "No predefined financial warning rule was triggered; "
            "review the financial statements and model score"
        )

    return "; ".join(reasons)


def main():
    df = pd.read_csv(INPUT_FILE)

    required = [
        "company",
        "year",
        "anomaly_status",
        "anomaly_score",
        "receivables_vs_revenue_growth_pp",
        "cash_flow_to_profit",
        "net_profit",
        "debt_to_equity",
    ]

    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    flagged = df[df["anomaly_status"] == "Potential anomaly"].copy()

    flagged["investigation_reason"] = flagged.apply(
        explain_record, axis=1
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    flagged.to_csv(OUTPUT_FILE, index=False)

    print(
        flagged[
            [
                "company",
                "year",
                "anomaly_score",
                "investigation_reason",
            ]
        ].to_string(index=False)
    )

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

