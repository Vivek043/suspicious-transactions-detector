def score_transaction(data: dict) -> float:
    # Dummy logic: flag high amount transactions
    amount = data.get("amount", 0)
    risk_score = min(amount / 1000, 1.0)
    return round(risk_score, 2)
