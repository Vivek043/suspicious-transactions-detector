def score_transaction(data: dict) -> float:
    amount = data.get("amount", 0)

    # If amount exceeds 10,000, assign max risk score
    if amount > 10000:
        return 1.0

    # Otherwise, scale risk score between 0 and 1
    risk_score = amount / 10000
    return round(risk_score, 2)
