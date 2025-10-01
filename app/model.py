from scripts.features import extract_features

def score_transaction(data: dict) -> float:
    """
    Score a transaction using feature extraction and a simple weighted model.
    Returns a risk score between 0.0 and 1.0.
    """
    features = extract_features(data)

    # Dummy model: weighted sum
    score = (
        0.6 * (features["amount"].values[0] / 10000)
        + 0.3 * features["location_risk"].values[0]
        + 0.1 * (features["hour"].values[0] / 24)
    )
    return round(min(score, 1.0), 2)
