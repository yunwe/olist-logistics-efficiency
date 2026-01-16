import pandas as pd
import logging
import os
from src.utils.read_datasets import read_customers, read_orders, read_orders_sellers

class CustomerSellerTransformer():
    def __init__(self, file_name):
        self.logger = logging.getLogger(__name__)
        self.output_dir = "data/output"
        self.save_path = os.path.join(self.output_dir, file_name)
    

    def run_all(self, force_run=False):
        if os.path.exists(self.save_path) and not force_run:
            return 

        """
        The main orchestrator for transformations. 
        It executes the steps in order.
        """
        df = read_orders()
        
        if df.empty:
            self.logger.warning("Received an empty DataFrame for Order Items.")
            return df
        df = self._remove_rows(df)
        df = self._merge_customers(df)
        df = self._merge_sellers(df)
        df = self._drop_columns(df)
        self._save_to_disk(df)
    
    def _remove_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        condition = df['order_status'] == 'delivered'
        df = df[condition]
        return df

    def _merge_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        c = read_customers()
        c = c[['customer_id', 'state', 'lat', 'lng']]
        c.columns = ['customer_id', 'cus_state', 'cus_lat', 'cus_lng']
        merge =  pd.merge(df, c, on='customer_id', how="left")
        return merge
    

    def _merge_sellers(self, df: pd.DataFrame) -> pd.DataFrame:
        s = read_orders_sellers()
        s = s[['order_id', 'seller_id', 'state', 'lat', 'lng']]
        s.columns = ['order_id', 'seller_id', 'seller_state', 'seller_lat', 'seller_lng']
        merge =  pd.merge(df, s, on='order_id', how="inner")
        return merge

    def _drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = ['order_status', 'customer_id', 'seller_id']
        df = df.drop(columns=cols, axis=1)
        return df
    
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)