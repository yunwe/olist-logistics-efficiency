import pandas as pd
import numpy as np

def flag_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Removes outliers from a dataframe based on the IQR method.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Calculate bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    

    #Flag outliers
    conditions = [
        df[column] < lower_bound,
        df[column] > upper_bound
    ]
    choices = [1, 1]

    df = df.copy()
    # The third argument is the default value (the 'else')
    df['outlier'] = np.select(conditions, choices, default=0)
    
    return df