import numpy as np
import pandas as pd

def clean_data(kc_data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean King County housing data.
    - Removes houses with 33 bedrooms.
    - Cleans and fills 'sqft_basement', 'view', and 'waterfront'.
    - Creates a 'lastknownchange' column and drops year columns.

    Args:
        kc_data (pd.DataFrame): Original dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    kc_data = kc_data[kc_data['bedrooms'] != 33]
    kc_data['sqft_basement'] = kc_data['sqft_basement'].replace('?', np.nan).astype(float)
    kc_data['sqft_basement'] = kc_data['sqft_living'] - kc_data['sqft_above']
    kc_data['view'] = kc_data['view'].fillna(0)
    kc_data['waterfront'] = kc_data['waterfront'].fillna(0)
    kc_data['lastknownchange'] = kc_data.apply(
        lambda x: x['yr_built'] if pd.isna(x['yr_renovated']) or x['yr_renovated'] == 0 else x['yr_renovated'],
        axis=1
    )
    kc_data = kc_data.drop(['yr_built', 'yr_renovated'], axis=1)
    return kc_data