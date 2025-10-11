# risk_scoring.py

import pandas as pd

def update_customer_score(customer_id, txn_score, history_df):
    # Get past scores
    past_scores = history_df[history_df['customer_id'] == customer_id]['risk_score'].values

    # Combine with new score
    all_scores = list(past_scores) + [txn_score]
    avg_score = sum(all_scores) / len(all_scores)

    # Normalize to 0–100
    normalized_score = min(max(avg_score, 0), 100)

    return round(normalized_score, 2)
