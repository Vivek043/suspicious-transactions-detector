import time
import requests

# Simulated transaction stream
transactions = [
    {"amount": 500, "timestamp": "2025-10-01 09:15:00", "location": "Dallas"},
    {"amount": 12000, "timestamp": "2025-10-01 14:30:00", "location": "HighRiskCountry1"},
    {"amount": 3000, "timestamp": "2025-10-01 02:00:00", "location": "Chicago"},
    {"amount": 9500, "timestamp": "2025-10-01 22:45:00", "location": "HighRiskCountry2"},
    {"amount": 15000, "timestamp": "2025-10-01 11:00:00", "location": "New York"},
]

for tx in transactions:
    response = requests.post("http://localhost:8000/score", json=tx)
    print(f"Transaction: {tx}")
    print(f"Risk Score: {response.json()['risk_score']}")
    print("-" * 40)
    time.sleep(2)  # Simulate delay between transactions
