# feedback_loop.py

import pandas as pd
import os

FEEDBACK_LOG = "data/feedback_log.csv"

def log_feedback(transaction_id, risk_score, decision, reasons):
    feedback_entry = {
        "transaction_id": transaction_id,
        "risk_score": risk_score,
        "decision": decision,  # "fraud" or "not_fraud"
        "reasons": ", ".join(reasons)
    }

    if os.path.exists(FEEDBACK_LOG):
        df = pd.read_csv(FEEDBACK_LOG)
        df = df.append(feedback_entry, ignore_index=True)
    else:
        df = pd.DataFrame([feedback_entry])

    df.to_csv(FEEDBACK_LOG, index=False)
    print(f"Logged feedback for TXN {transaction_id}: {decision}")
