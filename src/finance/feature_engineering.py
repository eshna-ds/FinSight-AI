
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "processed" / "financial_data.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "financial_features.csv"


def safe_divide(numerator, denominator):
    """Avoid invalid ratios when values are missing or denominator is zero."""
    if pd.isna(numerator) or pd.isna(denominator):
        return None

    if denominator == 0:
        return None

    return numerator / denominator


def main():
    # 1. Load financial data
    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "company",
        "year",
        "revenue",
        "net_profit",
        "total_debt",
        "receivables",
        "operating_cash_flow",
        "total_equity",
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    # 2. Sort each company's financial records by year
    df["year"] = pd.to_numeric(df["year"], errors="raise")
    df = df.sort_values(["company", "year"]).copy()

    # 3. Get previous-year values for the same company
    df["previous_revenue"] = (
        df.groupby("company")["revenue"].shift(1)
    )

    df["previous_receivables"] = (
        df.groupby("company")["receivables"].shift(1)
    )

    # 4. Calculate revenue growth (%)
    df["revenue_growth_pct"] = (
        (df["revenue"] - df["previous_revenue"])
        / df["previous_revenue"].where(
            df["previous_revenue"] > 0
        )
        * 100
    )

    # 5. Calculate receivables growth (%)
    df["receivables_growth_pct"] = (
        (df["receivables"] - df["previous_receivables"])
        / df["previous_receivables"].where(
            df["previous_receivables"] > 0
        )
        * 100
    )

    # 6. Calculate net profit margin (%)
    df["net_profit_margin_pct"] = (
        df["net_profit"]
        / df["revenue"].where(df["revenue"] != 0)
        * 100
    )

    # 7. Calculate debt-to-equity ratio
    df["debt_to_equity"] = (
        df["total_debt"]
        / df["total_equity"].where(
            df["total_equity"] > 0
        )
    )

    # 8. Compare operating cash flow with net profit
    df["cash_flow_to_profit"] = [
        safe_divide(cash_flow, profit)
        for cash_flow, profit in zip(
            df["operating_cash_flow"],
            df["net_profit"],
        )
    ]

    # 9. Calculate the cash-flow gap
    df["cash_flow_gap"] = (
        df["net_profit"] - df["operating_cash_flow"]
    )

    # 10. Compare receivables growth with revenue growth
    df["receivables_vs_revenue_growth_pp"] = (
        df["receivables_growth_pct"]
        - df["revenue_growth_pct"]
    )

    # 11. Save the engineered dataset
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    # 12. Display the important features
    columns_to_display = [
        "company",
        "year",
        "revenue_growth_pct",
        "receivables_growth_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "cash_flow_to_profit",
        "receivables_vs_revenue_growth_pp",
    ]

    print(df[columns_to_display].round(2).to_string(index=False))
    print(f"\nFeatures saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

