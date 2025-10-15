from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import joblib

# Import preprocessing
from features.feature_engineering import preprocess_transaction

# Load models
xgb_model = joblib.load("models/xgboost_classifier.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

# Initialize app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class Transaction(BaseModel):
    transaction_id: str
    source: str
    destination: str
    amount: float
    timestamp: str
    country: str
    currency: str

@app.post("/score")
async def score_transactions(payload: List[Dict]):
    df = pd.DataFrame(payload)

    # Dummy scoring logic
    df["xgb_score"] = 0.7
    df["xgb_flag"] = 1
    df["iso_flag"] = 0
    df["final_flag"] = 1
    df["reason"] = "High XGBoost score"

    df.fillna("missing", inplace=True)
    return df.to_dict(orient="records")
