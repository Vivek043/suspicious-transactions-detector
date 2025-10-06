import pandas as pd
import joblib

# Load trained pipeline (after you've saved it)
model = joblib.load('models/best_model.pkl')

def score_transaction(transaction_dict):
    """
    Accepts a dict with transaction features.
    Returns predicted label and risk probability.
    """
    df = pd.DataFrame([transaction_dict])
    prediction = model.predict(df)[0]
    proba = model.predict_proba(df)[0][1] if hasattr(model, 'predict_proba') else None
    return prediction, proba
