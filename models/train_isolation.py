import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load transaction data
df = pd.read_csv("data/transactions.csv")

# Add dummy features if missing
if 'tx_count_24h' not in df.columns:
    df['tx_count_24h'] = 5  # placeholder

if 'is_blacklisted' not in df.columns:
    df['is_blacklisted'] = 0  # placeholder

# Select features
features = df[["amount", "tx_count_24h", "is_blacklisted"]]

# Handle missing values
features = features.fillna(0)  # or use .dropna() to remove rows

# Train Isolation Forest
model = IsolationForest(random_state=42)
model.fit(features)

# Save model
joblib.dump(model, "models/isolation_forest.pkl")
print("✅ Isolation Forest model trained and saved successfully.")
