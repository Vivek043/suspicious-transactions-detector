from datetime import datetime

def calculate_risk_score(location, time, source_amount, destination_amount, source_name, destination_name):
    # Convert time to datetime if it's a string
    if isinstance(time, str):
        try:
            time = datetime.fromisoformat(time)
        except ValueError:
            try:
                time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Unrecognized time format: {time}")

    hour = time.hour

    # Convert amounts to float if they come in as strings
    try:
        source_amount = float(source_amount)
        destination_amount = float(destination_amount)
    except ValueError:
        raise ValueError("Transaction amounts must be numeric")

    risk_score = 0
    reasons = []

    # Rule 1: High amount
    if source_amount > 10000 or destination_amount > 10000:
        risk_score += 30
        reasons.append("High transaction amount")

    # Rule 2: Odd hours
    if hour < 6 or hour > 22:
        risk_score += 20
        reasons.append("Transaction during odd hours")

    # Rule 3: Suspicious location
    suspicious_locations = ['Russia', 'Iran', 'North Korea']
    if location in suspicious_locations:
        risk_score += 25
        reasons.append("Suspicious location")

    # Rule 4: Mismatched names
    if source_name.lower() == destination_name.lower():
        risk_score += 10
        reasons.append("Same source and destination name")

    # Normalize score
    risk_score = min(risk_score, 100)

    return risk_score, reasons
