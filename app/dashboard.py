import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from datetime import datetime
import os
import json
import pandas as pd
from logic.risk_score import calculate_risk_score
from simulator import stream_transactions

# Load sample transactions
sample_path = "data/notebooks/sample_transactions.csv"
df = pd.read_csv(sample_path, parse_dates=["Time"])

scored_transactions = []

for _, row in df.iterrows():
    score, reasons = calculate_risk_score(
        row["Amount"],
        row["Time"],
        row["Location"],
        row["Source"],
        row["Destination"],
        scored_transactions  # use scored history for repetition logic
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


def save_history(history, filename="data/transactions.json"):
    with open(filename, "w") as f:
        json.dump(history, f, default=str)

def load_history(filename="data/transactions.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
st.write("Current working directory:", os.getcwd())

st.set_page_config(page_title="Suspicious Transaction Dashboard", layout="wide")
st.title("Suspicious Transaction Compliance Dashboard")

# Simulated history
history = load_history()
save_history(history)

# Transaction Input
amount = st.number_input("Amount (USD)", min_value=0.0)
# Date and time inputs
date = st.date_input("Transaction Date", value=datetime.now().date())
time = st.time_input("Transaction Time", value=datetime.now().time())
# Combine into a single datetime object
transaction_time = datetime.combine(date, time)
location = st.text_input("Location")
source = st.text_input("Source Account")
destination = st.text_input("Destination Account")

if st.button("Submit Transaction"):
    risk_score, reasons = calculate_risk_score(
        amount, transaction_time, location, source, destination, history
    )

    new_tx = {
        "time": time,
        "amount": amount,
        "location": location,
        "source": source,
        "destination": destination,
        "risk_score": risk_score,
        "reasons": reasons
    }
    history.append(new_tx)

    st.subheader("Transaction Flagged")
    st.write(f"Risk Score: {risk_score}")
    st.write("Reasons:")
    for reason in reasons:
        st.markdown(f"- {reason}")
simulate = st.checkbox("Simulate Real-Time Transactions")

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

# History Table
st.subheader("Scored Sample Transactions")

for tx in scored_transactions:
    with st.expander(f"{tx['time']} | Score: {tx['risk_score']}"):
        st.write(f"Amount: ${tx['amount']}")
        st.write(f"Location: {tx['location']}")
        st.write(f"Source: {tx['source']}")
        st.write(f"Destination: {tx['destination']}")
        st.write("Reasons:")
        for reason in tx['reasons']:
            st.markdown(f"- {reason}")

        st.write(tx)
with st.sidebar:
    st.header("Explainability")
    st.write("Risk scores are calculated based on:")
    st.markdown("""
    - **Amount threshold**: Transactions over $100,000
    - **Time of day**: Off-hours (before 6 AM or after 10 PM)
    - **Location risk**: Flagged regions (e.g., New York, Miami, Dubai)
    - **Repetition**: Frequent destination accounts
    """)
st.subheader("Filter Transactions")
source_filter = st.text_input("Filter by Source Account")
location_filter = st.text_input("Filter by Location")

filtered_history = [
    tx for tx in history
    if (source_filter.lower() in tx['source'].lower()) and
       (location_filter.lower() in tx['location'].lower())
]

st.subheader("Filtered Results")
for tx in filtered_history:
    with st.expander(f"{tx['time']} | Score: {tx['risk_score']}"):
        st.write(tx)

#Save Flagged Transactions
def save_flagged(history, filename="data/flagged_transactions.json"):
    flagged = [tx for tx in history if tx["risk_score"] >= 0.5]
    with open(filename, "w") as f:
        json.dump(flagged, f, default=str)
save_flagged(history)
