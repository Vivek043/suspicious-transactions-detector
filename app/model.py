import pandas as pd

def score_transaction(data: dict) -> float:
    amount = data.get("amount", 0)
    location = data.get("location", "")
    timestamp = data.get("timestamp", "")
    source = data.get("source_account", "")
    destination = data.get("destination_account", "")

    score = 0.0
    if amount > 10000:
        score += 0.5
    if location in ["HighRiskCountry1", "HighRiskCountry2"]:
        score += 0.3
    hour = pd.to_datetime(timestamp).hour if timestamp else 0
    if hour in range(0, 6):
        score += 0.1
    if source == destination:
        score += 0.1

    return round(min(score, 1.0), 2)
