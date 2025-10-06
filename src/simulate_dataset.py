import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 10000
suspicious_ratio = 0.07  # 7% suspicious

# Helper functions
def random_country():
    return random.choice(['US', 'UK', 'IN', 'CN', 'RU', 'BR', 'NG', 'IR', 'DE', 'FR'])

def transaction_type():
    return random.choice(['wire', 'cash', 'crypto', 'card'])

def time_of_day():
    return random.choice(['morning', 'afternoon', 'night'])

def is_high_risk(country):
    return int(country in ['IR', 'RU', 'NG'])

# Generate data
data = []
for _ in range(n_samples):
    origin = random_country()
    dest = random_country()
    amt = np.round(np.random.exponential(scale=2000), 2)
    tx_type = transaction_type()
    time = time_of_day()
    age = np.random.randint(18, 80)
    acct_age = np.random.randint(10, 5000)
    prev_flags = np.random.poisson(0.5)
    label = np.random.choice([0, 1], p=[1 - suspicious_ratio, suspicious_ratio])

    data.append({
        'amount': amt,
        'origin_country': origin,
        'destination_country': dest,
        'transaction_type': tx_type,
        'time_of_day': time,
        'is_high_risk_country': is_high_risk(dest),
        'customer_age': age,
        'account_age_days': acct_age,
        'num_prev_flags': prev_flags,
        'label': label
    })

df = pd.DataFrame(data)
df.to_csv('simulated_transactions.csv', index=False)
print("✅ Dataset saved as simulated_transactions.csv")
