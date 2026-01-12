import pandas as pd
import logging
import os
from src.utils.read_datasets import read_customers, read_sellers
class GeolocationTransformer():
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

        df = self._add_zipcodes(df=df)
        df = self._fill_missing_values(df=df)
        self._save_to_disk(df=df)

    
    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.read_path,
                           dtype={'geolocation_zip_code_prefix': str})

    def _add_zipcodes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add Zipcodes from customers, sellers dataset to GeoLocation.
        Be ready for spatial analysis.
        """

        # Getting zipcodes
        seller_zipcodes = read_sellers()['seller_zip_code_prefix'].tolist()
        customer_zipcodes = read_customers()['customer_zip_code_prefix'].tolist()

        zipcodes = pd.DataFrame(seller_zipcodes + customer_zipcodes, columns = ["geolocation_zip_code_prefix"])

        # drop duplicates, so we have fewer rows for merge
        zipcodes = zipcodes.drop_duplicates()

        # Merge with geolocation df
        df = pd.merge(
                zipcodes, 
                df, 
                on = 'geolocation_zip_code_prefix', 
                how = 'outer'
            )
        
        # drop duplicates
        df = df.drop_duplicates(subset=['geolocation_zip_code_prefix'])
        return df
    
    def _fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        I tried finding the (lat, lng) value on google map by using the nearest zip_code. 
        Turn out they are not exactly correct. 
        I'll filled the missing values by using the nearest value.
        """

        df = df.sort_values(by='geolocation_zip_code_prefix')
        df = df.ffill()
        return df
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)