import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import sys, os
from datetime import datetime
from logic.risk_score import calculate_risk_score
from models.score import score_transaction
from logic.logger import log_transaction

from simulator import stream_transactions

# Custom CSS for compact UI
st.markdown("""
    <style>
        .reportview-container .main {
            padding-top: 10px;
            padding-right: 20px;
            padding-left: 20px;
            padding-bottom: 10px;
        }
        h1, h2, h3 {
            font-size: 20px;
        }
        .stButton button {
            padding: 0.25rem 0.75rem;
            font-size: 14px;
        }
        .stTextInput, .stNumberInput, .stDateInput, .stTimeInput {
            font-size: 14px;
        }
        .stExpander {
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar explainability
with st.sidebar:
    st.header("Why Transactions Are Flagged")
    st.markdown("""
    - High amount
    - Off-hours activity
    - Risky location
    - Repeated destination
    """)

# Load sample transactions
sample_path = "data/notebooks/sample_transactions.csv"
df = pd.read_csv(sample_path, parse_dates=["Time"])

# Score sample transactions
scored_transactions = []
for i, row in df.iterrows():
    score, reasons = calculate_risk_score(
        row["Amount"], row["Time"], row["Location"],
        row["Source"], row["Destination"], scored_transactions
    )
    scored_transactions.append({
        "time": row["Time"],
        "amount": row["Amount"],
        "location": row["Location"],
        "source": row["Source"],
        "destination": row["Destination"],
        "risk_score": score,
        "reasons": reasons
    })

# Initialize history
history = scored_transactions.copy()

# Title and summary
st.title("Suspicious Transaction Compliance Dashboard")
st.success(f"Total Transactions Scored: {len(history)}")
flagged = [tx for tx in history if tx["risk_score"] >= 0.5]
st.warning(f"Flagged Transactions: {len(flagged)}")

# Manual input section
st.subheader("Submit New Transaction")

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Amount (USD)", min_value=0.0, key="manual_amount")
    location = st.text_input("Location", key="manual_location")
    source = st.text_input("Source Account", key="manual_source")
    time_block = st.selectbox("Transaction Time Block", ["Morning (6–12)", "Afternoon (12–18)", "Evening (18–22)", "Night (22–6)"])
    destination = st.text_input("Destination Account", key="manual_destination")

with col2:
    date = st.date_input("Transaction Date", value=datetime.now().date(), key="manual_date")
    time = st.time_input("Transaction Time", value=datetime.now().time(), key="manual_time")


if st.button("Submit Transaction", key="manual_submit"):
    risk_score, reasons = calculate_risk_score(
        amount, time_block, location, source, destination, history
    )
    new_tx = {
        "time": time_block,
        "amount": amount,
        "location": location,
        "source": source,
        "destination": destination,
        "risk_score": risk_score,
        "reasons": reasons
    }
    history.append(new_tx)
    st.success(f"Transaction submitted with risk score: {risk_score}")
    for reason in reasons:
        st.markdown(f"- {reason}")

# Real-time simulation
simulate = st.checkbox("Simulate Real-Time Transactions", key="simulate_toggle")
if simulate:
    st.info("Streaming transactions...")
    for tx in stream_transactions():
        score, reasons = calculate_risk_score(
            tx["amount"], tx["time"], tx["location"],
            tx["source"], tx["destination"], history
        )
        tx["risk_score"] = score
        tx["reasons"] = reasons
        history.append(tx)

        st.write(f"New Transaction: {tx['time']} | Score: {score}")
        for reason in reasons:
            st.markdown(f"- {reason}")
#Section: Filters or Sidebar
source_filter = st.text_input("Source Account", key="filter_source")
location_filter = st.text_input("Location", key="filter_location")

# Save flagged transactions
def save_flagged(history, filename="data/flagged_transactions.json"):
    flagged = [tx for tx in history if tx["risk_score"] >= 0.5]
    with open(filename, "w") as f:
        json.dump(flagged, f, default=str)

save_flagged(history)

# Risk score distribution
st.subheader("Risk Score Distribution")
scores = [tx["risk_score"] for tx in history]
plt.hist(scores, bins=10, color="skyblue", edgecolor="black")
plt.xlabel("Score")
plt.ylabel("Frequency")
st.pyplot(plt)

# Expandable transaction history
with st.expander("View Flagged Transaction History", expanded=False):
    for i, tx in enumerate(flagged):
        with st.expander(f"{tx['time']} | Score: {tx['risk_score']}", expanded=False):
            st.write(f"Amount: ${tx['amount']}")
            st.write(f"Location: {tx['location']}")
            st.write(f"Source: {tx['source']}")
            st.write(f"Destination: {tx['destination']}")
            for reason in tx['reasons']:
                st.markdown(f"- {reason}")

#Scan Submitted Transaction
if st.button("Scan Submitted New Transaction"):
    transaction_dict = {
        "amount": float(st.session_state["source_amount"]),
        "origin_country": st.session_state["location"],
        "destination_country": st.session_state["location"],
        "transaction_type": "transfer",
        "time_of_day": st.session_state["time_block"],
        "customer_age": 35,
        "account_age_days": 400,
        "num_prev_flags": 0,
        "is_high_risk_country": st.session_state["location"].lower() in ["russia", "iran", "north korea"]
    }

    label, risk_proba = score_transaction(transaction_dict)
    st.success(f"ML Prediction: {'Suspicious' if label == 1 else 'Normal'} (Risk Probability: {risk_proba:.2f})")


    label, risk_proba = score_transaction(transaction_dict)
    st.success(f"ML Prediction: {'Suspicious' if label == 1 else 'Normal'} (Risk Probability: {risk_proba:.2f})")
# Rule-based scoring
rule_score, rule_reasons = calculate_risk_score(
    location,
    time_block,
    source_amount,
    destination_amount,
    source_name,
    destination_name
)

# ML scoring
label, risk_proba = score_transaction(transaction_dict)

# ✅ Log the transaction
log_transaction(
    transaction_dict,
    rule_score,
    rule_reasons,
    label,
    risk_proba
)

if st.button("Show Previous Transactions"):
    if os.path.exists("src/data/transaction_log.csv"):
        log_df = pd.read_csv("src/data/transaction_log.csv")
        st.dataframe(log_df.tail(20))
    else:
        st.info("No transactions logged yet.")
log_path = "src/data/transaction_log.csv"

if os.path.exists(log_path):
    log_df = pd.read_csv(log_path)

    st.subheader("📄 Filter Transactions")

    # Filter options
    risk_filter = st.selectbox("Filter by ML Risk Label", ["All", "Suspicious", "Normal"])
    location_filter = st.selectbox("Filter by Location", ["All"] + sorted(log_df["origin_country"].unique()))
    account_filter = st.selectbox("Filter by Source Account", ["All"] + sorted(log_df["source_account"].unique()))

    # Apply filters
    filtered_df = log_df.copy()

    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["ml_label"] == (1 if risk_filter == "Suspicious" else 0)]

    if location_filter != "All":
        filtered_df = filtered_df[filtered_df["origin_country"] == location_filter]

    if account_filter != "All":
        filtered_df = filtered_df[filtered_df["source_account"] == account_filter]

    st.dataframe(filtered_df.tail(50))
else:
    st.info("No transactions logged yet.")
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

# Display result
    st.success(f"ML Prediction: {'Suspicious' if label == 1 else 'Normal'} (Risk Probability: {risk_proba:.2f})")      

with st.form("transaction_form"):
    st.session_state["source_amount"] = st.text_input("Amount (USD)")
    st.session_state["location"] = st.text_input("Location")
    st.session_state["source_name"] = st.text_input("Source Account")
    st.session_state["destination_name"] = st.text_input("Destination Account")
    st.session_state["time_block"] = st.selectbox("Transaction Time Block", ["Morning (6–12)", "Afternoon (12–18)", "Evening (18–22)", "Night (22–6)"])
    submitted = st.form_submit_button("Submit Transaction")
if st.button("Show Previous Transactions"):
    log_path = "src/data/transaction_log.csv"
    if os.path.exists(log_path):
        log_df = pd.read_csv(log_path)
        st.subheader("📄 Recent Transactions")
        st.dataframe(log_df.tail(20))  # Show last 20 entries
    else:
        st.info("No transactions logged yet.")

