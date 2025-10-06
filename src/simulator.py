import random
import time
import pandas as pd

def stream_transactions(n=10, delay=2):
    """
    Simulates streaming transactions one by one.
    Yields a dictionary for each transaction.
    """
    countries = ["USA", "Russia", "Iran", "Germany", "India"]
    times = ["Morning (6–12)", "Afternoon (12–18)", "Evening (18–22)", "Night (22–6)"]
    types = ["transfer", "withdrawal", "deposit"]

    for _ in range(n):
        tx = {
            "amount": round(random.expovariate(1/5000), 2),
            "origin_country": random.choice(countries),
            "destination_country": random.choice(countries),
            "transaction_type": random.choice(types),
            "time_of_day": random.choice(times),
            "customer_age": random.randint(18, 80),
            "account_age_days": random.randint(30, 2000),
            "num_prev_flags": random.randint(0, 3),
            "is_high_risk_country": False  # can be set later
        }
        tx["is_high_risk_country"] = tx["origin_country"].lower() in ["russia", "iran", "north korea"]
        yield tx
        time.sleep(delay)
