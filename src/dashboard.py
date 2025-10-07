import streamlit as st
import pandas as pd
import os
from logic.risk_score import calculate_risk_score
from models.score import score_transaction
from logic.logger import log_transaction

st.set_page_config(page_title="Suspicious Transaction Compliance Dashboard", layout="wide")
st.title("🚨 Suspicious Transaction Compliance Dashboard")

# Notification bars
st.success("Valid Transactions Count: 10")
st.warning("Flagged Transactions: 1")

# --- Transaction Form ---
with st.form("transaction_form"):
    st.subheader("Submit New Transaction")
    st.session_state["source_amount"] = st.text_input("Amount (USD)", value="1000")
    st.session_state["transaction_date"] = st.date_input("Transaction Date")
    st.session_state["location"] = st.text_input("Location", value="NY")
    st.session_state["transaction_time"] = st.text_input("Transaction Time", value="14:00")
    st.session_state["source_account"] = st.text_input("Source Account")
    st.session_state["destination_account"] = st.text_input("Destination Account")
    st.session_state["transaction_threshold"] = st.text_input("Transaction Threshold")
    submitted = st.form_submit_button("Submit Transaction")

# --- Scoring and Logging ---
if submitted:
    source_amount = st.session_state["source_amount"]
    location = st.session_state["location"]
    source_name = st.session_state["source_account"]
    destination_name = st.session_state["destination_account"]
    time_block = st.session_state["transaction_time"]

    transaction_dict = {
        "amount": float(source_amount),
        "origin_country": location,
        "destination_country": location,
        "transaction_type": "transfer",
        "time_of_day": time_block,
        "customer_age": 35,
        "account_age_days": 400,
        "num_prev_flags": 0,
        "source_account": source_name,
        "destination_account": destination_name,
        "is_high_risk_country": location.lower() in ["russia", "iran", "north korea"]
    }

    rule_score, rule_reasons = calculate_risk_score(
        location,
        time_block,
        source_amount,
        source_amount,  # assuming destination_amount = source_amount
        source_name,
        destination_name
    )

    label, risk_proba = score_transaction(transaction_dict)

    log_transaction(
        transaction_dict,
        rule_score,
        rule_reasons,
        label,
        risk_proba
    )

    st.success(f"ML Prediction: {'Suspicious' if label == 1 else 'Normal'} (Risk Probability: {risk_proba:.2f})")

# --- Transaction History Viewer ---
log_path = "src/data/transaction_log.csv"
if os.path.exists(log_path):
    log_df = pd.read_csv(log_path)

    st.subheader("📄 Filter Transactions")

    risk_filter = st.selectbox("Filter by ML Risk Label", ["All", "Suspicious", "Normal"])
    location_filter = st.selectbox("Filter by Location", ["All"] + sorted(log_df["origin_country"].unique()))
    account_filter = st.selectbox("Filter by Source Account", ["All"] + sorted(log_df["source_account"].unique()))

    filtered_df = log_df.copy()

    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["ml_label"] == (1 if risk_filter == "Suspicious" else 0)]

    if location_filter != "All":
        filtered_df = filtered_df[filtered_df["origin_country"] == location_filter]

    if account_filter != "All":
        filtered_df = filtered_df[filtered_df["source_account"] == account_filter]

    st.dataframe(filtered_df.tail(50))

    # --- Export Flagged Transactions ---
    import io
    if not filtered_df.empty and st.button("📤 Export Flagged Transactions"):
        flagged_df = filtered_df[filtered_df["ml_label"] == 1]
        if not flagged_df.empty:
            csv_buffer = io.StringIO()
            flagged_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download CSV",
                data=csv_buffer.getvalue(),
                file_name="flagged_transactions.csv",
                mime="text/csv"
            )
        else:
            st.info("No flagged transactions to export.")
else:
    st.info("No transactions logged yet.")
