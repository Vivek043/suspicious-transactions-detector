import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Dashboard", "Flagged Transactions", "Settings"])

# Backend URL
BACKEND_URL = "http://localhost:8000/score"

# Header
st.title("💼 Fraud Detection Dashboard")

# Load sample transactions (replace with real input later)
sample_data = pd.read_csv("data/transactions.csv")
sample_payload = sample_data.to_dict(orient="records")

# Score transactions
@st.cache_data(ttl=60)
def get_scored_data(payload):
    try:
        response = requests.post(BACKEND_URL, json=payload)
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Backend error: {e}")
        return pd.DataFrame()

scored_df = get_scored_data(sample_payload)
if scored_df.empty or "final_flag" not in scored_df.columns:
    st.error("⚠️ Backend response missing 'final_flag'. Check for NaNs or scoring logic.")
    st.stop()
st.write("Returned columns:", scored_df.columns.tolist())
st.dataframe(scored_df.head())

# Dashboard Section
if section == "Dashboard":
    st.subheader("📊 Overview")

    total_txns = len(scored_df)
    flagged_txns = scored_df["final_flag"].sum()
    last_refresh = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", total_txns)
    col2.metric("Flagged Transactions", flagged_txns)
    col3.metric("Last Refresh", last_refresh)

    # Reason breakdown
    st.markdown("### 🚨 Reasons for Flagging")
    reason_counts = scored_df[scored_df["final_flag"] == 1]["reason"].value_counts()
    st.bar_chart(reason_counts)

    # Risk score trend
    st.markdown("### 📈 Risk Score Trend")
    if "xgb_score" in scored_df.columns:
        st.line_chart(scored_df["xgb_score"])

# Flagged Transactions Section

elif section == "Flagged Transactions":
    st.subheader("🚩 Flagged Transactions")
    flagged = scored_df[scored_df["final_flag"] == 1]
    st.markdown("### 🔍 Filter Flagged Transactions")
    st.markdown("### 🔄 Real-Time Mode")
    auto_refresh = st.checkbox("Enable Auto-Refresh (every 30 seconds)")
    if auto_refresh:
        st.experimental_rerun()

    # Risk score threshold
    score_threshold = st.slider("Minimum Risk Score", min_value=0.0, max_value=1.0, value=0.6, step=0.05)
    # Country filter
    countries = flagged["destination_country"].dropna().unique().tolist()
    selected_country = st.selectbox("Destination Country", ["All"] + countries)
    # Reason filter
    reasons = flagged["reason"].dropna().unique().tolist()
    selected_reason = st.selectbox("Reason for Flagging", ["All"] + reasons)
    # Apply filters
    filtered = flagged[
        (flagged["xgb_score"] >= score_threshold) &
        ((flagged["destination_country"] == selected_country) if selected_country != "All" else True) &
        ((flagged["reason"] == selected_reason) if selected_reason != "All" else True)
    ]
    st.markdown("### 📤 Export Filtered Results")

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Transactions as CSV",
        data=csv,
        file_name="flagged_transactions.csv",
        mime="text/csv"
    )
    st.markdown("### 🧠 Explainability Panel")

    for idx, row in filtered.iterrows():
        with st.expander(f"Transaction {idx + 1} — Risk Score: {row['xgb_score']:.2f}"):
            st.write(f"**Amount:** ${row['amount']}")
            st.write(f"**Source → Destination:** {row['source']} → {row['destination']}")
            st.write(f"**Final Flag:** {'✅ Suspicious' if row['final_flag'] == 1 else '❌ Normal'}")
            st.write(f"**Reasons for Flagging:** {row['reason']}")
            st.write(f"**Model Flags:** XGBoost: {row['xgb_flag']}, Isolation Forest: {row['iso_flag']}")



# Settings Section
elif section == "Settings":
    st.subheader("⚙️ Settings")

    st.markdown("### 📤 Export All Flagged Transactions")
    csv_all = flagged.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download All Flagged Transactions as CSV",
        data=csv_all,
        file_name="flagged_transactions.csv",
        mime="text/csv"
    )

    st.markdown("### 🔄 Real-Time Mode")
    auto_refresh_settings = st.checkbox("Enable Auto-Refresh (every 30 seconds)")
    if auto_refresh_settings:
        st.experimental_rerun()

    st.markdown("### ⚙️ Model Settings")

    # Risk score threshold
    new_threshold = st.slider("Risk Score Threshold", 0.0, 1.0, 0.6, 0.05)
    st.session_state["risk_threshold"] = new_threshold

    # Model toggle
    model_choice = st.radio("Model Selection", ["Hybrid", "XGBoost Only", "Isolation Forest Only"])
    st.session_state["model_choice"] = model_choice

    st.success("Settings saved. These will apply on next refresh.")
    st.write("Returned columns:", scored_df.columns.tolist())
    st.dataframe(scored_df.head())
