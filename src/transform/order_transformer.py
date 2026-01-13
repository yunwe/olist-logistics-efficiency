import pandas as pd
import logging
import os

class OrderTransformer():
    def __init__(self, file_name):
        self.logger = logging.getLogger(__name__)
        self.raw_dir = "data/raw"
        self.output_dir = "data/output"
        self.read_path = os.path.join(self.raw_dir, file_name)
        self.save_path = os.path.join(self.output_dir, file_name)
    

    def run_all(self, force_run=False):
        if os.path.exists(self.save_path) and not force_run:
            return 

        """
        The main orchestrator for transformations. 
        It executes the steps in order.
        """
        df = self._read_file()

        if df.empty:
            self.logger.warning("Received an empty DataFrame for Order transformation.")
            return df

        df = self._add_columns(df=df)
        self._save_to_disk(df=df)

    
    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.read_path,
                    parse_dates=[
                         'order_purchase_timestamp', 
                         'order_approved_at',
                         'order_delivered_carrier_date',
                         'order_delivered_customer_date',
                         'order_estimated_delivery_date'
                    ])
    
    def _add_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df['total_delivery_time'] = df['order_delivered_customer_date'] - df['order_purchase_timestamp']
        df['estimated_delivery_time'] = df['order_estimated_delivery_date'] - df['order_purchase_timestamp']
        df['wait_approve_time'] = df['order_approved_at'] - df['order_purchase_timestamp']
        df['seller_to_logistic_time'] = df['order_delivered_carrier_date'] - df['order_approved_at']
        df['logistic_to_customer_time'] = df['order_delivered_customer_date'] - df['order_delivered_carrier_date']
        return df
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)