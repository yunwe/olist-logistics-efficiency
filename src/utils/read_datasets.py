import pandas as pd

def read_state_name_lookup() -> pd.DataFrame:
    return pd.read_csv("data/processed/state_name_lookup.csv")