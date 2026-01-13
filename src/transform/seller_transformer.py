import pandas as pd
import logging
import os
from src.utils.read_datasets import read_geolocation

class SellerTransformer():
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
            self.logger.warning("Received an empty DataFrame for Seller transformation.")
            return df

        df = self._add_lat_lng(df)
        df = self._clean_column_names(df)
        self._save_to_disk(df=df)

    
    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.read_path, dtype={'seller_zip_code_prefix': str})
    
    def _add_lat_lng(self, df: pd.DataFrame) -> pd.DataFrame:
        geolocation = read_geolocation()
        df = pd.merge(df, geolocation, left_on ='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
        df = df.drop(['geolocation_zip_code_prefix', 'geolocation_city', 'geolocation_state'], axis = 1)
        return df

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = ['seller_id', 'zip_code', 'city', 'state', 'lat', 'lng']
        return df
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)