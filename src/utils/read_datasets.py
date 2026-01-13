import pandas as pd

def read_state_name_lookup() -> pd.DataFrame:
    return pd.read_csv("data/processed/state_name_lookup.csv")

def read_geolocation() -> pd.DataFrame:
    return pd.read_csv("data/processed/olist_geolocation_dataset.csv", dtype={'geolocation_zip_code_prefix': str}) 

def read_customers() -> pd.DataFrame:
    return pd.read_csv("data/output/olist_customers_dataset.csv", dtype={'zip_code': str})

def read_sellers() -> pd.DataFrame:
    return pd.read_csv("data/output/olist_sellers_dataset.csv", dtype={'zip_code': str})

def read_orders() -> pd.DataFrame:
    df = pd.read_csv("data/output/olist_orders_dataset.csv", parse_dates=[
                         'order_purchase_timestamp', 
                         'order_approved_at',
                         'order_delivered_carrier_date',
                         'order_delivered_customer_date',
                         'order_estimated_delivery_date'])
    df['total_delivery_time'] = pd.to_timedelta(df['total_delivery_time'])
    df['estimated_delivery_time'] = pd.to_timedelta(df['estimated_delivery_time'])
    df['wait_approve_time'] = pd.to_timedelta(df['wait_approve_time'])
    df['seller_to_logistic_time'] = pd.to_timedelta(df['seller_to_logistic_time'])    
    df['logistic_to_customer_time'] = pd.to_timedelta(df['logistic_to_customer_time'])    
    return df

 


def read_order_items() -> pd.DataFrame:
    return pd.read_csv("data/raw/olist_order_items_dataset.csv", parse_dates=['shipping_limit_date'])


    
