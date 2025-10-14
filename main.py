# main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from utils.feature_engineering import preprocess_transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
xgb_model = joblib.load("models/xgboost_classifier.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

# Load history data
history_df = pd.read_csv("data/transactions.csv")

@app.post("/score")
async def score_transaction(request: Request):
    try:
        payload = await request.json()
        txn_df = pd.DataFrame(payload)

        # Normalize column names
        txn_df = txn_df.rename(columns={
            "source_account": "source",
            "destination_account": "destination",
            "source_id": "source",
            "destination_id": "destination"
        })

        # Feature engineering
        features = preprocess_transaction(txn_df, history_df)

        # Model scoring
        xgb_scores = xgb_model.predict_proba(features)[:, 1]
        xgb_flags = (xgb_scores > 0.5).astype(int)
        iso_flags = [1 if f == -1 else 0 for f in iso_model.predict(features)]

        results = pd.DataFrame({
            "xgb_score": xgb_scores,
            "xgb_flag": xgb_flags,
            "iso_flag": iso_flags,
            "final_flag": [max(x, i) for x, i in zip(xgb_flags, iso_flags)]
        })

        return results.to_dict(orient="records")

    except Exception as e:
        print("❌ Backend error:", e)
        return [{"error": str(e)}]
