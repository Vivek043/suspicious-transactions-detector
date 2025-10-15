from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from features.feature_engineering import preprocess_transaction

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

def get_flag_reason(row):
    reasons = []
    if row["amount"] > 10000:
        reasons.append("Large transfer")
    if row["country_risk_score"] > 1.0:
        reasons.append("High-risk country")
    if row["is_blacklisted"] == 1:
        reasons.append("Blacklisted account")
    if row["geo_distance"] > 5000:
        reasons.append("Unusual geo distance")
    return ", ".join(reasons) if reasons else "Normal"

@app.post("/score")
async def score_transaction(request: Request):
    try:
        payload = await request.json()
        txn_df = pd.DataFrame(payload)

        # Normalize and rename columns
        txn_df.columns = txn_df.columns.str.strip().str.lower()
        txn_df = txn_df.rename(columns={
            "source_account": "source",
            "source_id": "source",
            "account_number": "source",
            "destination_account": "destination",
            "destination_id": "destination",
            "receiver_account": "destination",
            "dest_account": "destination"
        })

        required_cols = ["source", "destination", "amount", "source_lat", "source_lon", "destination_lat", "destination_lon", "destination_country"]
        missing = [col for col in required_cols if col not in txn_df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Feature engineering
        expected_features = ["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]
        features = preprocess_transaction(txn_df, history_df)
        features = features[expected_features].fillna(0)

        # Model scoring
        xgb_scores = xgb_model.predict_proba(features)[:, 1]
        xgb_flags = (xgb_scores > 0.5).astype(int)
        iso_flags = [1 if f == -1 else 0 for f in iso_model.predict(features)]
        final_flags = [1 if (score > 0.6 or iso == 1) else 0 for score, iso in zip(xgb_scores, iso_flags)]

        # Combine results
        combined = features.copy()
        combined["xgb_score"] = xgb_scores
        combined["xgb_flag"] = xgb_flags
        combined["iso_flag"] = iso_flags
        combined["final_flag"] = final_flags
        combined["reason"] = combined.apply(get_flag_reason, axis=1)

        return combined.to_dict(orient="records")

    except Exception as e:
        return [{"error": str(e)}]
