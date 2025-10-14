# streamlit_app.py

import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Suspicious Transaction Detector", layout="wide")
st.title("🚨 Suspicious Transaction Detector")

# Load new transactions
try:
    txn_df = pd.read_csv("data/new_transactions.csv")
except FileNotFoundError:
    st.error("❌ Could not find 'data/new_transactions.csv'. Please add test transactions.")
    st.stop()

# Display raw input
st.subheader("📥 Incoming Transactions")
st.dataframe(txn_df, width='stretch')

# Send to FastAPI backend
with st.spinner("Scoring transactions..."):
    try:
        response = requests.post("http://localhost:8000/score", json=txn_df.to_dict(orient="records"))
        results = pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"❌ Failed to connect to FastAPI backend: {e}")
        st.stop()

# Combine input + results
scored_df = pd.concat([txn_df.reset_index(drop=True), results.reset_index(drop=True)], axis=1)

# Display results
st.subheader("📊 Scored Transactions")
st.dataframe(scored_df, width='stretch')

# Highlight flagged transactions
st.subheader("🚩 Flagged Transactions")
flagged = scored_df[scored_df["final_flag"] == 1]
st.dataframe(flagged, width='stretch')

# Optional: Download results
st.download_button("📥 Download Results as CSV", data=scored_df.to_csv(index=False), file_name="scored_transactions.csv")
