import pandas as pd
import time

def stream_transactions(path="data/notebooks/sample_transactions.csv", delay=2):
    df = pd.read_csv(path, parse_dates=["Time"])
    for _, row in df.iterrows():
        yield {
            "time": row["Time"],
            "amount": row["Amount"],
            "location": row["Location"],
            "source": row["Source"],
            "destination": row["Destination"]
        }
        time.sleep(delay)
