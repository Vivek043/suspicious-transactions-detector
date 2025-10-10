#This module will transform raw transaction data into enriched features  for model input.
# feature_engineering.py

import pandas as pd
import numpy as np
from geopy.distance import geodesic

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
