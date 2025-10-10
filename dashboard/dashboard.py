import streamlit as st
import pandas as pd
from models.model_inference import score_transaction
from utils.feature_engineering import preprocess_transaction

st.title("Suspicious Transaction Detector")

# Simulated input
txn_input = {
    "amount": 12000,
    "timestamp": "2025-10-10 13:15:00",
    "location": "Mumbai",
    "source_account": "ACC123",
    "destination_account": "ACC999",
    "destination_country": "IN"
}
txn_df = pd.DataFrame([txn_input])

# Feature engineering
features = preprocess_transaction(txn_df)

# Score transaction
result = score_transaction(features)

# Display results
st.subheader("Transaction Risk Assessment")
st.metric("Risk Score", result["risk_score"])
st.write("Flagged:", result["flagged"])
st.write("Reasons:", ", ".join(result["reasons"]))

if result["flagged"]:
    st.button("Generate SAR Report")
