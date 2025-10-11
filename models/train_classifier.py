import pandas as pd
import xgboost as xgb
import joblib

# Load your transaction data
df = pd.read_csv("data/transactions.csv")

# Add dummy labels for now (replace with real labels later)
df["label"] = 0
df.loc[df["amount"] > 10000, "label"] = 1  # flag large transfers as fraud

# Add dummy features if missing
if 'tx_count_24h' not in df.columns:
    df['tx_count_24h'] = 5

if 'is_blacklisted' not in df.columns:
    df['is_blacklisted'] = 0

# Select features and target
features = df[["amount", "tx_count_24h", "is_blacklisted"]]
target = df["label"]

# Handle missing values
features = features.fillna(0)

# Train XGBoost classifier
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(features, target)

# Save model
joblib.dump(model, "models/xgboost_classifier.pkl")
print("✅ XGBoost classifier saved successfully.")
