import pandas as pd
import logging
import os
from abc import abstractmethod
from src.utils.read_datasets import read_state_name_lookup

class PopulationTransformer:
    def __init__(self, file_name):
        self.logger = logging.getLogger(__name__)
        self.raw_dir = "data/raw"
        self.output_dir = "data/output"
        self.save_path = os.path.join(self.output_dir, file_name)
        self.read_path = os.path.join(self.raw_dir, file_name)

    def run_all(self):
        """
        The main orchestrator for transformations. 
        It executes the steps in order.
        """
        df = self._read_file()

        if df.empty:
            self.logger.warning("Received an empty DataFrame for transformation.")
            return df

        df = self._drop_columns(df=df)
        df = self._clean_column_names(df=df)
        df = self._convert_data_types(df=df)
        df = self._add_state_id(df=df)
        self._save_to_disk(df=df)

    
    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.read_path)
    
    @abstractmethod
    def _drop_columns(self, df: pd.DataFrame)-> pd.DataFrame:
        pass

    @abstractmethod
    def _clean_column_names(self, df: pd.DataFrame)-> pd.DataFrame:
        pass


    def _convert_data_types(self, df: pd.DataFrame)-> pd.DataFrame:
        """Ensures numbers are actually numbers, not strings."""
        # Remove commas from population numbers (e.g., "1,000" -> 1000)
        if 'population' in df.columns:
            df['population'] = df['population'].replace({',': ''}, regex=True).astype(int)
        return df

    def _add_state_id(self, df: pd.DataFrame)-> pd.DataFrame:
        lookup = read_state_name_lookup()
        df = pd.merge(df, lookup, left_on = "state", right_on = "state_name", how = "outer")
        df = df.drop('state', axis = 1)
        return df
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        df.to_csv(self.save_path, index=False)


class PopulationStatesTransformer(PopulationTransformer):
    def _drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        selected_columns = [df.columns[1], df.columns[3]]
        return df[selected_columns].copy()

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = ['state', 'population']
        return df
    
class PopulationCitiesTransformer(PopulationTransformer):
    def _drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        selected_columns = [df.columns[0], df.columns[1], df.columns[3]]
        return df[selected_columns].copy()

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = ['city', 'state', 'population']
        return df