import pandas as pd

def read_state_name_lookup() -> pd.DataFrame:
    return pd.read_csv("data/processed/state_name_lookup.csv")

def read_customers() -> pd.DataFrame:
    return pd.read_csv("data/raw/olist_customers_dataset.csv", dtype={'customer_zip_code_prefix': str})

def read_sellers() -> pd.DataFrame:
    return pd.read_csv("data/raw/olist_sellers_dataset.csv", dtype={'seller_zip_code_prefix': str})