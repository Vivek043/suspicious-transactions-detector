from datetime import datetime

def calculate_risk_score(location, time, source_amount, destination_amount, source_name, destination_name):
    # --- Step 1: Convert time to datetime ---
    if isinstance(time, str):
        try:
            time = datetime.fromisoformat(time)
        except ValueError:
            try:
                time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                time = datetime.now()  # fallback if format is unknown

    hour = time.hour

    # --- Step 2: Convert amounts to float ---
    try:
        source_amount = float(source_amount)
        destination_amount = float(destination_amount)
    except (ValueError, TypeError):
        source_amount = 0.0
        destination_amount = 0.0

    # --- Step 3: Normalize names ---
    source_name = str(source_name).strip().lower()
    destination_name = str(destination_name).strip().lower()

    # --- Step 4: Risk scoring rules ---
    risk_score = 0
    reasons = []

    # Rule 1: High transaction amount
    if source_amount > 10000 or destination_amount > 10000:
        risk_score += 30
        reasons.append("High transaction amount")

    # Rule 2: Odd transaction hours
    if hour < 6 or hour > 22:
        risk_score += 20
        reasons.append("Transaction during odd hours")

    # Rule 3: Suspicious location
    suspicious_locations = ['russia', 'iran', 'north korea']
    if location.strip().lower() in suspicious_locations:
        risk_score += 25
        reasons.append("Suspicious location")

    # Rule 4: Same source and destination name
    if source_name == destination_name:
        risk_score += 10
        reasons.append("Same source and destination name")

    # --- Step 5: Cap score ---
    risk_score = min(risk_score, 100)

    return risk_score, reasons
