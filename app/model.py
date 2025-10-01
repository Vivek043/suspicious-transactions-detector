'''def score_transaction(data: dict) -> float:
    amount = data.get("amount", 0)

    # If amount exceeds 10,000, assign max risk score
    if amount > 10000:
        return 1.0

    # Otherwise, scale risk score between 0 and 1
    risk_score = amount / 10000
    return round(risk_score, 2)'''
from scripts.features import extract_features

def score_transaction(data: dict) -> float:
    features = extract_features(data)

    # Dummy model: weighted sum
    score = (
        0.6 * (features["amount"].values[0] / 10000) +
        0.3 * features["location_risk"].values[0] +
        0.1 * (features["hour"].values[0] / 24)
    )
    return round(min(score, 1.0), 2)
