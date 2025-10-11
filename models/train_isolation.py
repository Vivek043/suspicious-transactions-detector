import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load your transaction data
df = pd.read_csv("data/transactions.csv")

# Add dummy features if missing
df["tx_count_24h"] = df.get("tx_count_24h", pd.Series([5] * len(df)))
df["is_blacklisted"] = df.get("is_blacklisted", pd.Series([0] * len(df)))

# Select features
features = df[["amount", "tx_count_24h", "is_blacklisted"]].fillna(0)

# Train Isolation Forest
model = IsolationForest(random_state=42)
model.fit(features)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/isolation_forest.pkl")
print("✅ Isolation Forest model trained and saved.")
