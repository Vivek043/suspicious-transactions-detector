# stream_simulator.py
import sys
import os
import pandas as pd
import time
history_df = pd.read_csv("data/transactions.csv")
features = preprocess_transaction(pd.DataFrame([txn]), history_df)
# Add repo root to sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from models.model_inference import score_transaction
from utils.feature_engineering import preprocess_transaction
def stream_transactions(csv_path, delay=2):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        txn_df = pd.DataFrame([row])
        features = preprocess_transaction(txn_df)
        result = score_transaction(features)

        print(f"TXN {row['transaction_id']} → Risk: {result['risk_score']} | Flagged: {result['flagged']} | Reasons: {result['reasons']}")
        time.sleep(delay)
if __name__ == "__main__":
    stream_transactions("data/transactions.csv", delay=2)