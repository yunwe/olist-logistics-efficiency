import pandas as pd
import logging
import os
from src.utils.read_datasets import read_order_items, read_sellers, read_orders
from src.utils.helper import flag_outliers_iqr

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
        df = self._remove_errors(df)
        df = self._flag_outliers(df)
        self._save_to_disk(df=df)
    

    def _merge_sellers(self, df: pd.DataFrame) -> pd.DataFrame:
        sellers = read_sellers()
        merge =  pd.merge(df, sellers, on='seller_id', how="left")
        merge = merge[['order_id', 'seller_id', 'shipping_limit_date', 
                       'zip_code', 'state', 'lat', 'lng']]
        return merge
    
    def _merge_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        orders = read_orders()
        
        # Calcualte total time need from purchase to delivered to carrier
        orders['delivered_carrier_time'] = orders['order_delivered_carrier_date'] - orders['order_purchase_timestamp']
        
        # Remove the orders that are not delivered yet
        orders = orders[orders['order_delivered_carrier_date'].notnull()]

        df = pd.merge(df, orders[['order_id', 'order_purchase_timestamp', 'delivered_carrier_time']] , on='order_id', how="inner")
        return df
    
    def _remove_errors(self, df: pd.DataFrame) -> pd.DataFrame:
        condition_to_keep = df['delivered_carrier_time'].dt.total_seconds() > 0
        return df[condition_to_keep]

    def _flag_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        The delivery time varies state by state.
        So, the outlier is detected per state instead of the whold dataset.
        """
        states = df['state'].value_counts().index
        flaged = pd.DataFrame()
        for state in states:
            new_df = flag_outliers_iqr(df[df['state'] == state], 'delivered_carrier_time')
            flaged = pd.concat([flaged, new_df], ignore_index=True)
            
        return flaged
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)