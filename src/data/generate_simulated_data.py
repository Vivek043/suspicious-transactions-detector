import pandas as pd
import numpy as np
import os

np.random.seed(42)

n = 5000
df = pd.DataFrame({
    "amount": np.random.exponential(scale=5000, size=n).round(2),
    "origin_country": np.random.choice(["USA", "Russia", "Iran", "Germany", "India"], size=n),
    "destination_country": np.random.choice(["USA", "Russia", "Iran", "Germany", "India"], size=n),
    "transaction_type": np.random.choice(["transfer", "withdrawal", "deposit"], size=n),
    "time_of_day": np.random.choice(["Morning (6–12)", "Afternoon (12–18)", "Evening (18–22)", "Night (22–6)"], size=n),
    "customer_age": np.random.randint(18, 80, size=n),
    "account_age_days": np.random.randint(30, 2000, size=n),
    "num_prev_flags": np.random.poisson(0.5, size=n),
})

# Add label: 1 = suspicious, 0 = normal
df["is_high_risk_country"] = df["origin_country"].isin(["Russia", "Iran", "North Korea"])
df["label"] = (
    (df["amount"] > 10000).astype(int) |
    (df["time_of_day"] == "Night (22–6)").astype(int) |
    df["is_high_risk_country"].astype(int)
)

os.makedirs("src/data", exist_ok=True)
df.to_csv("src/data/simulated_transactions.csv", index=False)
print("✅ Simulated data saved to src/data/simulated_transactions.csv")
