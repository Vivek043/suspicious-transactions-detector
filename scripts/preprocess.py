import pandas as pd

def clean_data(filepath):
    df = pd.read_csv(filepath)
    df.dropna(inplace=True)
    df["amount"] = df["amount"].astype(float)
    return df
