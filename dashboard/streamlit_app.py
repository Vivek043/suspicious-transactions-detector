import streamlit as st
import requests
import pandas as pd

st.write("Streamlit app loaded ✅")

st.set_page_config(page_title="Compliance Dashboard", layout="wide")
st.title("🛡️ Suspicious Transaction Compliance Dashboard")

# Sample transaction input
st.sidebar.header("Transaction Input")

amount = st.sidebar.number_input("Amount", min_value=0.0)
timestamp = st.sidebar.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)", value="2025-10-01 14:30:00")
location = st.sidebar.selectbox("Location", ["New York", "Chicago", "Dallas", "HighRiskCountry1", "HighRiskCountry2"])
source_account = st.sidebar.text_input("Source Account", value="CUST001")
destination_account = st.sidebar.text_input("Destination Account", value="CUST847")


if st.sidebar.button("Submit Transaction"):
    payload = {
        "amount": amount,
        "timestamp": timestamp,
        "location": location,
        "source_account": source_account,
        "destination_account": destination_account
    }

    response = requests.post("http://localhost:8000/score", json=payload)
    risk_score = response.json()["risk_score"]

    # Explainability logic
    reasons = []
    if amount > 10000:
        reasons.append("Amount exceeds ₹10,000 threshold")
    if location in ["HighRiskCountry1", "HighRiskCountry2"]:
        reasons.append("Location flagged as high-risk")
    hour = pd.to_datetime(timestamp).hour
    if hour in range(0, 6):
        reasons.append("Transaction occurred during unusual hours")

    st.subheader("🚨 Transaction Flagged")
    st.metric("Risk Score", f"{risk_score}")
    st.write("**Reasons for Flagging:**")
    for reason in reasons:
        st.write(f"- {reason}")

    # Save to session state for history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "amount": amount,
        "timestamp": timestamp,
        "location": location,
        "risk_score": risk_score,
        "reasons": "; ".join(reasons)
    })

# Display history
if "history" in st.session_state and st.session_state.history:
    st.subheader("📁 Flagged Transaction History")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    # Optionally re-check the last submitted transaction (safe-guard)
    last = st.session_state.history[-1]
    try:
        response = requests.post("http://localhost:8000/score", json={
            "amount": last["amount"],
            "timestamp": last["timestamp"],
            "location": last["location"]
        })
        response.raise_for_status()
        result = response.json()
        st.write(f"Risk Score (live): {result.get('risk_score', 'N/A')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
