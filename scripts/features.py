import pandas as pd

def extract_features(transaction: dict) -> pd.DataFrame:
    # Example features: amount, hour of day, location risk
    amount = transaction.get("amount", 0)
    timestamp = transaction.get("timestamp", "")
    location = transaction.get("location", "")

    hour = pd.to_datetime(timestamp).hour if timestamp else 0
    location_risk = 1 if location in ["HighRiskCountry1", "HighRiskCountry2"] else 0

    features = pd.DataFrame([{
        "amount": amount,
        "hour": hour,
        "location_risk": location_risk
    }])
    return features
