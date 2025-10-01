import streamlit as st
import requests

st.title("Suspicious Transaction Detector")

amount = st.number_input("Transaction Amount", min_value=0.0)
if st.button("Score Transaction"):
    response = requests.post("http://localhost:8000/score", json={"amount": amount})
    st.write(f"Risk Score: {response.json()['risk_score']}")
