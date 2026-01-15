import pandas as pd
import logging
import os
from src.utils.read_datasets import read_order_items, read_orders, read_products

class ProductShippingTimeTransformer():
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
        df = self._sum_quantity(df)
        df = self._merge_products(df)
        df = self._merge_orders(df)
        df = self._remove_errors(df)
        self._save_to_disk(df=df)
    

    def _merge_products(self, df: pd.DataFrame) -> pd.DataFrame:
        p = read_products()
        cols = ['product_id', 'product_category_name']
        merge =  pd.merge(df, p[cols], on='product_id', how="left")
        return merge
    
    def _merge_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        orders = read_orders()

        # Remove the orders that are not delivered to carrier yet
        orders = orders[orders['order_delivered_carrier_date'].notnull()]

        # Remove the orders that are not delivered to customers yet
        orders = orders[orders['order_delivered_customer_date'].notnull()]
        
        # Calcualte total time need for delivery
        orders['delivered_carrier_time'] = orders['order_delivered_carrier_date'] - orders['order_purchase_timestamp']
        orders['carrier_to_customer_time'] = orders['order_delivered_customer_date'] - orders['order_delivered_carrier_date']
        orders['total_delivery_time'] = orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
        

        df = pd.merge(df, orders[
                    [
                        'order_id', 'order_purchase_timestamp', 'delivered_carrier_time',
                        'carrier_to_customer_time', 'total_delivery_time'
                    ]
                ],
                on='order_id', how="inner")
        return df
    
    def _remove_errors(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df['delivered_carrier_time'].dt.total_seconds() > 0]
        df = df[df['carrier_to_customer_time'].dt.total_seconds() > 0]
        df = df[df['total_delivery_time'].dt.total_seconds() > 0]
        
        return df

    def _sum_quantity(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.groupby(['order_id', 'product_id']).agg({
            'order_item_id': 'sum',
            'seller_id': 'first',
            'price': 'first',
            'freight_value': 'first'
        }).reset_index()
        df.columns = ['order_id', 'product_id', 'quantity', 'seller_id', 'price', 'freight_value']
        return df


    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)