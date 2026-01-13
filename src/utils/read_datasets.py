import pandas as pd

def read_state_name_lookup() -> pd.DataFrame:
    return pd.read_csv("data/processed/state_name_lookup.csv")

def read_customers() -> pd.DataFrame:
    return pd.read_csv("data/raw/olist_customers_dataset.csv", dtype={'customer_zip_code_prefix': str})

def read_sellers() -> pd.DataFrame:
    return pd.read_csv("data/raw/olist_sellers_dataset.csv", dtype={'seller_zip_code_prefix': str})

def read_orders() -> pd.DataFrame:
    return pd.read_csv("data/output/olist_orders_dataset.csv", parse_dates=[
                         'order_purchase_timestamp', 
                         'order_approved_at',
                         'order_delivered_carrier_date',
                         'order_delivered_customer_date',
                         'order_estimated_delivery_date'])
    
