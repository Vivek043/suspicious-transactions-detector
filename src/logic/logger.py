import pandas as pd
import os
from datetime import datetime

LOG_PATH = "src/data/transaction_log.csv"

def log_transaction(data, rule_score, rule_reasons, ml_label, ml_proba):
    """
    Appends a transaction to the log CSV.
    """
    entry = data.copy()
    entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry["rule_score"] = rule_score
    entry["rule_reasons"] = "; ".join(rule_reasons)
    entry["ml_label"] = ml_label
    entry["ml_proba"] = round(ml_proba, 4)

    df = pd.DataFrame([entry])
    if os.path.exists(LOG_PATH):
        df.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_PATH, index=False)
