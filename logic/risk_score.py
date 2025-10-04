from datetime import datetime

def calculate_risk_score(amount, time, location, source, destination, history):
    score = 0.0
    reasons = []

    # Amount threshold
    if amount > 100000:
        score += 0.3
        reasons.append("Amount exceeds $100,000 threshold")

    # Off-hours transaction
    hour = time.hour
    if hour < 6 or hour > 22:
        score += 0.2
        reasons.append("Transaction during off-hours")

    # High-risk location
    flagged_locations = ["New York", "Miami", "Dubai"]
    if location in flagged_locations:
        score += 0.1
        reasons.append(f"Location flagged: {location}")

    # Repeated destination
    recent_destinations = [tx['destination'] for tx in history[-5:]]
    if recent_destinations.count(destination) > 2:
        score += 0.2
        reasons.append("Repeated destination account")

    return round(score, 2), reasons
