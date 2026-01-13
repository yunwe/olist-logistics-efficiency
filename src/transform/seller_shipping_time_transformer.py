import pandas as pd
import logging
import os
from src.utils.read_datasets import read_order_items, read_sellers, read_orders

class SellerShippingTimeTransformer():
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
        df = read_order_items()
        
        if df.empty:
            self.logger.warning("Received an empty DataFrame for Order Items.")
            return df

        df = self._merge_sellers(df)
        df = self._merge_orders(df)
        self._save_to_disk(df=df)
    

    def _merge_sellers(self, df: pd.DataFrame) -> pd.DataFrame:
        sellers = read_sellers()
        merge =  pd.merge(df, sellers, on='seller_id', how="left")
        merge = merge[['order_id', 'seller_id', 'shipping_limit_date', 
                       'zip_code', 'state', 'lat', 'lng']]
        return merge
    
    def _merge_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        orders = read_orders()
        df = pd.merge(df, orders[['order_id', 'order_purchase_timestamp', 'seller_to_logistic_time']] , on='order_id', how="left")
        return df
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)