
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "processed"

ANOMALY_FILE = DATA_DIR / "anomaly_results.csv"
REPORT_FILE = DATA_DIR / "investigation_results.csv"

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📊",
    layout="wide",
)

st.title("FinSight AI")
st.subheader("Financial Intelligence & Anomaly Investigation")
st.caption("Anomaly detection is a warning system, not proof of fraud.")

if not ANOMALY_FILE.exists():
    st.error("Anomaly results not found. Run the anomaly detection script first.")
    st.stop()

df = pd.read_csv(ANOMALY_FILE)

if df.empty:
    st.warning("No financial records available.")
    st.stop()

flagged = df[df["anomaly_status"] == "Potential anomaly"].copy()

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Potential Anomalies", len(flagged))
col3.metric(
    "Records Not Flagged",
    (df["anomaly_status"] == "Not flagged").sum(),
)

st.divider()

# Anomaly chart
st.subheader("Anomaly Scores by Company and Year")

chart_data = df.copy()
chart_data["Record"] = (
    chart_data["company"].astype(str)
    + " - "
    + chart_data["year"].astype(str)
)

st.bar_chart(chart_data.set_index("Record")["anomaly_score"])

# All financial records
st.subheader("All Analyzed Records")
st.dataframe(df, width="stretch")

# Investigation details
st.subheader("Investigation Findings")

if REPORT_FILE.exists():
    report = pd.read_csv(REPORT_FILE)

    if not report.empty:
        st.dataframe(report, width="stretch")
    else:
        st.info("No flagged records were found for investigation.")
else:
    st.info(
        "Investigation report not found. "
        "Run Step 8 before viewing investigation findings."
    )
