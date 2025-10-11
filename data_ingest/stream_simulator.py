# stream_simulator.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.model_inference import score_transaction
from utils.feature_engineering import preprocess_transaction
import pandas as pd
import time



def stream_transactions(csv_path, delay=2):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        txn_df = pd.DataFrame([row])
        features = preprocess_transaction(txn_df)
        result = score_transaction(features)

        print(f"TXN {row['transaction_id']} → Risk: {result['risk_score']} | Flagged: {result['flagged']} | Reasons: {result['reasons']}")
        time.sleep(delay)
