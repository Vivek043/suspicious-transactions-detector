# retrain_xgb.py

import pandas as pd
import joblib
from xgboost import XGBClassifier
from utils.feature_engineering import preprocess_transaction

# Load labeled data
df = pd.read_csv("data/labeled_transactions.csv")
history_df = pd.read_csv("data/transactions.csv")

# Feature engineering
features = preprocess_transaction(df, history_df)

# Select full feature set
X = features[["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]]
y = df["label"]
print("✅ Columns in training DataFrame:", X.columns.tolist())
print("✅ Sample row:", X.iloc[0])
# Train model
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X, y)

# Save model
joblib.dump(model, "models/xgboost_classifier.pkl")
print("✅ Model retrained and saved to models/xgboost_classifier.pkl")
