from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "processed" / "investigation_results.csv"
CSV_OUTPUT = ROOT / "data" / "processed" / "investigation_report.csv"
MD_OUTPUT = ROOT / "data" / "processed" / "investigation_report.md"


def main():
    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("No flagged records found.")
        return

    df["recommended_action"] = (
        "Review annual reports and verify financial figures"
    )

    columns = [
        "company",
        "year",
        "anomaly_score",
        "investigation_reason",
        "recommended_action",
    ]

    report = df[columns].sort_values("anomaly_score")

    CSV_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(CSV_OUTPUT, index=False)

    lines = [
        "# FinSight AI - Financial Investigation Report",
        "",
        f"Records requiring investigation: {len(report)}",
        "",
        "> An anomaly is a warning signal, not proof of fraud.",
        "",
    ]

    for _, row in report.iterrows():
        lines.extend([
            f"## {row['company']} - {row['year']}",
            f"- Anomaly score: {row['anomaly_score']:.4f}",
            f"- Warning: {row['investigation_reason']}",
            f"- Next action: {row['recommended_action']}",
            "",
        ])

    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print("Investigation report generated successfully!")
    print(f"CSV report: {CSV_OUTPUT}")
    print(f"Readable report: {MD_OUTPUT}")


if __name__ == "__main__":
    main()
