#This module will transform raw transaction data into enriched features  for model input.
# feature_engineering.py

import pandas as pd
import numpy as np
from geopy.distance import geodesic
from datetime import timedelta
country_risk_df = pd.read_csv("data/country_risk.csv")
country_risk_dict = dict(zip(country_risk_df["country"], country_risk_df["risk_score"]))

blacklist = pd.read_csv("data/blacklist.csv")["account"].tolist()
def compute_geo_distance(lat1, lon1, lat2, lon2):
    try:
        return geodesic((lat1, lon1), (lat2, lon2)).km
    except:
        return 0.0

def add_rolling_features(df):
    df = df.sort_values(by='timestamp')
    df['tx_count_24h'] = df.groupby('account_id')['timestamp'].transform(
        lambda x: x.rolling('24h').count()
    )
    return df

def compute_amount_zscore(df):
    df['amount_zscore'] = df.groupby('account_id')['amount'].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    return df

def geo_distance(row, prev_location):
    try:
        return geodesic(row['location'], prev_location).km
    except:
        return np.nan

def add_geo_features(df):
    df['geo_distance'] = df.apply(lambda row: geo_distance(row, row.get('prev_location')), axis=1)
    return df

def enrich_with_external_risk(df, country_risk_dict, blacklist):
    df['country_risk'] = df['destination_country'].map(country_risk_dict)
    df['is_blacklisted'] = df['destination_account'].isin(blacklist).astype(int)
    return df

#pre_processing_transaction
def preprocess_transaction(txn_df: pd.DataFrame, history_df: pd.DataFrame) -> pd.DataFrame:
    txn_df = txn_df.copy()

    # Ensure timestamp is datetime
    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
    txn_df["timestamp"] = pd.to_datetime(txn_df["timestamp"])

    # Compute tx_count_24h
    tx_counts = []
    for _, row in txn_df.iterrows():
        src = row["source"]
        (history_df["source"] == src)
        ts = row["timestamp"]
        past_24h = history_df[
            (history_df["source"] == src) &
            (history_df["timestamp"] >= ts - timedelta(hours=24)) &
            (history_df["timestamp"] < ts)
        ]
        tx_counts.append(len(past_24h))
    txn_df["tx_count_24h"] = tx_counts

    # Compute is_blacklisted
    txn_df["is_blacklisted"] = txn_df.apply(
        lambda row: int(row["source"] in blacklist or row["destination"] in blacklist),
        axis=1
    )

    # Compute geo_distance
    geo_distances = []
    for _, row in txn_df.iterrows():
        lat1 = row.get("source_lat", 0.0)
        lon1 = row.get("source_lon", 0.0)
        lat2 = row.get("destination_lat", 0.0)
        lon2 = row.get("destination_lon", 0.0)
        dist = compute_geo_distance(lat1, lon1, lat2, lon2)
        geo_distances.append(dist)
    txn_df["geo_distance"] = geo_distances
    txn_df["country_risk_score"] = txn_df["destination_country"].map(country_risk_dict).fillna(0)

    # Final feature set
    features = txn_df[["amount", "tx_count_24h", "is_blacklisted", "geo_distance", "country_risk_score"]].fillna(0)
    return features


