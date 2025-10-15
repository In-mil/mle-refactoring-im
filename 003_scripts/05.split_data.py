from sklearn.model_selection import train_test_split
import pandas as pd

def split_data(df: pd.DataFrame, target: str = "price") -> tuple:
    """
    - Drops columns from leakage/unused list.
    - Creates feature and target variables.
    - Splits data into train and test sets.

    Args:
        df (pd.DataFrame): Input DataFrame after cleaning and feature engineering.
        target (str): Name of target variable; default 'price'.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    # Leakage/unused columns
    droplst = ['price', 'sqftprice', 'date', 'deltalat', 'deltalong']
    feature_cols = [col for col in df.columns if col not in droplst]
    X = df[feature_cols]
    y = df[target]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("X_train shape:", X_train.shape)
    print("y_train shape:", y_train.shape)
    print("X_test shape:", X_test.shape)
    print("y_test shape:", y_test.shape)

    # Shows first rows as in notebook
    print("First rows of X_train:\n", X_train.head())

    return X_train, X_test, y_train, y_test

    #X_train, X_test, y_train, y_test = split_data(kc_data)