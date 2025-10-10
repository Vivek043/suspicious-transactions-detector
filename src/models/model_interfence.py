# model_inference.py

import joblib
import numpy as np
import pandas as pd

# Load models
anomaly_model = joblib.load('models/isolation_forest.pkl')
classifier_model = joblib.load('models/xgboost_classifier.pkl')

def score_transaction(features: pd.DataFrame) -> dict:
    # Anomaly score (scaled 0–100)
    anomaly_raw = anomaly_model.decision_function(features)
    anomaly_score = (1 - anomaly_raw) * 100

    # Classification probability
    class_prob = classifier_model.predict_proba(features)[0][1] * 100

    # Final risk score (weighted average)
    final_score = 0.6 * class_prob + 0.4 * anomaly_score

    # Flag reason logic
    reasons = []
    if final_score > 80:
        if features['amount'].values[0] > 10000:
            reasons.append("Large transfer")
        if features['tx_count_24h'].values[0] > 10:
            reasons.append("Unusual frequency")
        if features['is_blacklisted'].values[0] == 1:
            reasons.append("Blacklisted account")

    return {
        "risk_score": round(final_score, 2),
        "flagged": final_score > 80,
        "reasons": reasons
    }
