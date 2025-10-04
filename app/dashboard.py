import streamlit as st
from datetime import datetime
from logic.risk_score import calculate_risk_score
import os
st.write("Current working directory:", os.getcwd())

st.set_page_config(page_title="Suspicious Transaction Dashboard", layout="wide")
st.title("Suspicious Transaction Compliance Dashboard")

# Simulated history
history = []

st.title("Suspicious Transaction Compliance Dashboard")

# Transaction Input
amount = st.number_input("Amount (USD)", min_value=0.0)
time = st.datetime_input("Time", value=datetime.now())
location = st.text_input("Location")
source = st.text_input("Source Account")
destination = st.text_input("Destination Account")

if st.button("Submit Transaction"):
    risk_score, reasons = calculate_risk_score(
        amount, time, location, source, destination, history
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

# History Table
st.subheader("Flagged Transaction History")
for tx in history:
    with st.expander(f"{tx['time']} | Score: {tx['risk_score']}"):
        st.write(tx)