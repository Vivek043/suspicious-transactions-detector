from datetime import datetime
def calculate_risk_score(location, time_block, source_amount, destination_amount, source_name, destination_name):
    # --- Step 1: Convert amounts to float ---
    try:
        source_amount = float(source_amount)
        destination_amount = float(destination_amount)
    except (ValueError, TypeError):
        source_amount = 0.0
        destination_amount = 0.0

    # --- Step 2: Normalize names and location ---
    source_name = str(source_name).strip().lower()
    destination_name = str(destination_name).strip().lower()
    location = str(location).strip().lower()

    # --- Step 3: Risk scoring rules ---
    risk_score = 0
    reasons = []

    # Rule 1: High transaction amount
    if source_amount > 10000 or destination_amount > 10000:
        risk_score += 30
        reasons.append("High transaction amount")

    # Rule 2: Odd transaction hours
    if time_block == "Night (22–6)":
        risk_score += 20
        reasons.append("Transaction during odd hours")

    # Rule 3: Suspicious location
    suspicious_locations = ['russia', 'iran', 'north korea']
    if location in suspicious_locations:
        risk_score += 25
        reasons.append("Suspicious location")

    # Rule 4: Same source and destination name
    if source_name == destination_name:
        risk_score += 10
        reasons.append("Same source and destination name")

    # --- Step 4: Cap score ---
    risk_score = min(risk_score, 100)

    return risk_score, reasons
