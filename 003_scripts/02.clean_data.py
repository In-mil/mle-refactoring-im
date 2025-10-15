import numpy as np
import pandas as pd

def clean_king_county_data(kc_data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean King County housing data.
    - Removes houses with 33 bedrooms.
    - Cleans and fills 'sqftbasement', 'view', and 'waterfront'.
    - Creates a 'lastknownchange' column and drops year columns.

    Args:
        kc_data (pd.DataFrame): Original dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    kc_data = kc_data[kc_data['bedrooms'] != 33]
    kc_data['sqftbasement'] = kc_data['sqftbasement'].replace('?', np.nan).astype(float)
    kc_data['sqftbasement'] = kc_data['sqftliving'] - kc_data['sqftabove']
    kc_data['view'] = kc_data['view'].fillna(0)
    kc_data['waterfront'] = kc_data['waterfront'].fillna(0)
    kc_data['lastknownchange'] = kc_data.apply(
        lambda x: x['yrbuilt'] if pd.isna(x['yrrenovated']) or x['yrrenovated'] == 0 else x['yrrenovated'],
        axis=1
    )
    kc_data = kc_data.drop(['yrbuilt', 'yrrenovated'], axis=1)
    return kc_data