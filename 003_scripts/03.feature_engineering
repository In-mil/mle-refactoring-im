import numpy as np
import pandas as pd

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds engineered features to the King County housing DataFrame based on notebook logic.

    - Price per square foot
    - Distance to city center (Medina, WA)
    - Minimum distance to a waterfront property (waterdistance)

    Args:
        df (pd.DataFrame): Cleaned input dataframe.

    Returns:
        pd.DataFrame: DataFrame with new features.
    """
    # Price per square foot of living area
    df['sqftprice'] = (df['price'] / df['sqftliving']).round(2)
    
    # Center coordinates (Medina, WA)
    center_lat, center_long = 47.62774, -122.24194
    df['deltalat'] = np.abs(center_lat - df['lat'])
    df['deltalong'] = np.abs(center_long - df['long'])
    
    # Distance to city center
    df['centerdistance'] = (
        df['deltalong'] * np.cos(np.radians(center_lat)) +
        df['deltalat']
    ) * (2122 / (np.pi * 6378 / 360))
    
    # Prepare waterlist (all waterfront houses)
    waterlist = df[df['waterfront'] == 1][['lat', 'long']].values

    # Function to compute distance (from notebook)
    def calc_min_waterdistance(row, waterlist):
        distances = []
        for ref_long, ref_lat in waterlist:
            deltalong = row['long'] - ref_long
            deltalat = row['lat'] - ref_lat
            deltalongcorr = deltalong * np.cos(np.radians(ref_lat))
            # identical multiplier to notebook's simplified "distance"
            dist = (deltalongcorr ** 2 + deltalat ** 2) * (2122 / (np.pi * 6378 / 360))
            distances.append(dist)
        return min(distances) if distances else np.nan

    # Calculate min waterdistance for each row (can be slow for large datasets)
    df['waterdistance'] = df.apply(
        lambda row: calc_min_waterdistance(row, waterlist)
        if row['waterfront'] == 0 else 0.0, axis=1
    )

    return df

#kc_data = engineer_features(kc_data)