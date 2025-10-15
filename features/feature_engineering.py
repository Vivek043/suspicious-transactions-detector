import pandas as pd
import numpy as np
from geopy.distance import geodesic

def calculate_geo_distance(row):
    try:
        source_coords = (row["source_lat"], row["source_lon"])
        dest_coords = (row["destination_lat"], row["destination_lon"])
        return geodesic(source_coords, dest_coords).km
    except:
        return np.nan

def enrich_with_external_risk(df, country_risk_dict, blacklist):
    df["country_risk_score"] = df["destination_country"].map(country_risk_dict).fillna(0)
    df["is_blacklisted"] = df["destination"].isin(blacklist).astype(int)
    return df

def preprocess_transaction(txn_df, history_df):
    txn_df["tx_count_24h"] = txn_df["source"].map(
        history_df.groupby("source")["timestamp"].count()
    ).fillna(0)

    txn_df["geo_distance"] = txn_df.apply(calculate_geo_distance, axis=1)

    country_risk_dict = {
        "NG": 1.5, "IR": 1.3, "PK": 1.2, "RU": 1.1,
        "US": 0.2, "GB": 0.3, "CA": 0.3, "DE": 0.4
    }
    blacklist = ["acct_999", "acct_888", "acct_777"]

    txn_df = enrich_with_external_risk(txn_df, country_risk_dict, blacklist)

    txn_df.fillna(0, inplace=True)  # ✅ Critical fix

    return txn_df
