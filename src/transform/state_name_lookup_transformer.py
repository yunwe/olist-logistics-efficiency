import pandas as pd
import logging
import os


class StateNameTransformer():
    def __init__(self, file_name):
        self.logger = logging.getLogger(__name__)
        self.raw_dir = "data/raw"
        self.output_dir = "data/processed"
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
            self.logger.warning("Received an empty DataFrame for transformation.")
            return df

        df = self._drop_columns(df=df)
        df = self._drop_rows(df=df)
        df = self._clean_column_names(df=df)
        df = self._replace_names(df=df)
        self._save_to_disk(df=df)
    
    def _read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.read_path)
    
    def _drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        selected_columns = [df.columns[0], df.columns[1]]
        return df[selected_columns].copy()
    
    def _drop_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove 1st, 2nd rows.
        Which are original titles from webpage.
        """
        return df.drop([0, 1], axis = 0)

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = ['state_id', 'state_name']
        return df
    
    def _replace_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Replace the state names to match with population datasets.
        """
        df['state_name'] = df['state_name'].replace('SãoPaulo', 'São Paulo')
        df['state_name'] = df['state_name'].replace('MinasGerais', 'Minas Gerais')
        df['state_name'] = df['state_name'].replace('Riode Janeiro', 'Rio de Janeiro')
        df['state_name'] = df['state_name'].replace('RioGrande do Sul', 'Rio Grande do Sul')
        df['state_name'] = df['state_name'].replace('SantaCatarina', 'Santa Catarina')
        df['state_name'] = df['state_name'].replace('EspíritoSanto', 'Espírito Santo')
        df['state_name'] = df['state_name'].replace('MatoGrosso', 'Mato Grosso')
        df['state_name'] = df['state_name'].replace('RioGrande do Norte', 'Rio Grande do Norte')
        df['state_name'] = df['state_name'].replace('MatoGrossodo Sul', 'Mato Grosso do Sul')
        df['state_name'] = df['state_name'].replace('DistritoFederal', 'Distrito Federal')
        return df
    
    def _save_to_disk(self, df: pd.DataFrame) -> None:
        os.makedirs(self.raw_dir, exist_ok=True)
        df.to_csv(self.save_path, index=False)
    
