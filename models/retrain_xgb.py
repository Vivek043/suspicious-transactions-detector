# retrain_xgb.py

import pandas as pd
import joblib
from xgboost import XGBClassifier
from utils.feature_engineering import preprocess_transaction

# Load labeled data
df = pd.read_csv("data/labeled_transactions.csv")  # must include 'label' column

# Feature engineering
history_df = pd.read_csv("data/transactions.csv")
features = preprocess_transaction(df, history_df)

# Match features to full set
X = features[["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]]
y = df["label"]

# Train model
model = XGBClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "models/xgboost_classifier.pkl")
