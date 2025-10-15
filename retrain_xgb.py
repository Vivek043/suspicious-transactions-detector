import pandas as pd
import joblib
from xgboost import XGBClassifier
from utils.feature_engineering import preprocess_transaction

# Load historical data
df = pd.read_csv("data/transactions.csv")

# Simulate history for feature engineering
history_df = df.copy()
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

# Apply full preprocessing pipeline
features = preprocess_transaction(df, history_df)

# Select expected features
expected_features = ["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]
# Simulate labels
df["label"] = ((df["amount"] > 10000) | (df["destination_country"] == "NG")).astype(int)

# Preprocess
features = preprocess_transaction(df, df.copy())
X = features[["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]].fillna(0)
y = df["label"]

# Train
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X, y)

# Save
joblib.dump(model, "models/xgboost_classifier.pkl")
print("✅ Model retrained and saved to models/xgboost_classifier.pkl")

