import pandas as pd
import joblib
from xgboost import XGBClassifier
from features.feature_engineering import preprocess_transaction

# Load and normalize training data
df = pd.read_csv("data/transactions.csv")
df.columns = df.columns.str.strip().str.lower()
df = df.rename(columns={
    "source_account": "source",
    "source_id": "source",
    "account_number": "source",
    "destination_account": "destination",
    "destination_id": "destination",
    "receiver_account": "destination",
    "dest_account": "destination"
})

# Simulate labels
df["label"] = ((df["amount"] > 10000) | (df["destination_country"] == "NG")).astype(int)

# Feature engineering
features = preprocess_transaction(df, df.copy())
X = features[["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]].fillna(0)
y = df["label"]

# Train model
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X, y)

# Save model
joblib.dump(model, "models/xgboost_classifier.pkl")
print("✅ Model retrained and saved to models/xgboost_classifier.pkl")
