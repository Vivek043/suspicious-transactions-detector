from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import joblib

# Import preprocessing logic
from features.feature_engineering import preprocess_transaction

# Load models
xgb_model = joblib.load("models/xgboost_classifier.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

# Define FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema
class Transaction(BaseModel):
    transaction_id: str
    source: str
    destination: str
    amount: float
    timestamp: str
    country: str
    currency: str
    # Add any other fields your pipeline expects

@app.post("/score")
async def score_transactions(payload: List[Dict]):
    # Convert payload to DataFrame
    df = pd.DataFrame(payload)

    # Preprocess input
    df = preprocess_transaction(df)

    # Select features
    xgb_features = [col for col in df.columns if col.startswith("feat_")]
    iso_features = xgb_features  # Assuming same features for both

    # Score with XGBoost
    xgb_scores = xgb_model.predict_proba(df[xgb_features])[:, 1]
    xgb_flags = (xgb_scores > 0.6).astype(int)

    # Score with Isolation Forest
    iso_raw = iso_model.predict(df[iso_features])
    iso_flags = [1 if val == -1 else 0 for val in iso_raw]

    # Final flag logic
    final_flags = [1 if (xgb > 0.6 or iso == 1) else 0 for xgb, iso in zip(xgb_scores, iso_flags)]

    # Reason generator
    def get_flag_reason(row):
        reasons = []
        if row["xgb_score"] > 0.6:
            reasons.append("High XGBoost score")
        if row["iso_flag"] == 1:
            reasons.append("Isolation Forest anomaly")
        return ", ".join(reasons) if reasons else "No anomaly"

    # Add results to DataFrame
    df["xgb_score"] = xgb_scores
    df["xgb_flag"] = xgb_flags
    df["iso_flag"] = iso_flags
    df["final_flag"] = final_flags
    df["reason"] = df.apply(get_flag_reason, axis=1)

    # Return scored data
    return df.to_dict(orient="records")
