# main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from utils.feature_engineering import preprocess_transaction

app = FastAPI()

# Allow Streamlit frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
xgb_model = joblib.load("models/xgboost_classifier.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

# Load history data for feature engineering
history_df = pd.read_csv("data/transactions.csv")

@app.post("/score")
async def score_transaction(request: Request):
    payload = await request.json()
    txn_df = pd.DataFrame(payload)

    # Feature engineering
    features = preprocess_transaction(txn_df, history_df)

    # XGBoost prediction
    xgb_scores = xgb_model.predict_proba(features)[:, 1]
    xgb_flags = (xgb_scores > 0.5).astype(int)

    # Isolation Forest prediction
    iso_flags = iso_model.predict(features)
    iso_flags = [1 if f == -1 else 0 for f in iso_flags]

    # Combine results
    results = pd.DataFrame({
        "xgb_score": xgb_scores,
        "xgb_flag": xgb_flags,
        "iso_flag": iso_flags,
        "final_flag": [max(x, i) for x, i in zip(xgb_flags, iso_flags)]
    })
    print("Received payload:", txn_df.head())
    print("Features:", features.head())
    print("Scoring complete.")

    return results.to_dict(orient="records")
