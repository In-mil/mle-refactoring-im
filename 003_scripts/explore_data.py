import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def explore_data(df: pd.DataFrame) -> None:
    """
    - Shows basic info and missing values.
    - Shows value counts and unique values for important columns.
    - Plots histograms, boxplots, pairplots, and correlation heatmap.
    """
    # Shape and Info
    print("Data shape:", df.shape)
    print("\nData info:")
    print(df.info())

    # Missing Value Check
    missing_values = pd.DataFrame(df.isnull().sum(), columns=['count'])
    missing_values['percentage'] = (missing_values['count']/df.shape[0]*100).round(2)
    print("\nMissing values (count and %):\n", missing_values[missing_values['count'] != 0])

    # Value Counts for selected categorical columns
    for col in ['view', 'waterfront']:
        print(f"\nValue counts for {col}:")
        print(df[col].value_counts())

    # Unique values for all columns
    print("\nNumber of unique values per column:")
    print(df.nunique())

    # Summary Statistics
    print("\nSummary statistics:")
    print(df.describe().round(2))

    # Histograms for selected variables
    columns_histogram = [
        'price',
        'bathrooms',
        'bedrooms',
        'floors',
        'grade',
        'sqft_living',
        'sqft_lot'
    ]
    # Only include lastknownchange if it exists
    if 'lastknownchange' in df.columns:
        columns_histogram.append('lastknownchange')

    print("\nPlotting histograms...")
    df[columns_histogram].hist(bins=50, figsize=(20, 15))
    plt.show()

    # Boxplot for price
    print("\nPlotting boxplot for price...")
    # Log-Transformation der Preise (füge neue Spalte hinzu)
    df['log_price'] = np.log(df['price'])

    plt.figure(figsize=(10, 6))
    sns.boxplot(y=df['log_price'])
    plt.title("Boxplot of log(House Prices)")
    plt.ylabel("log(Price)")
    plt.show()

    # Scatterplots for price and sqftprice vs. distance to center/water
    if 'centerdistance' in df.columns and 'waterdistance' in df.columns:
        print("\nScatter plot: price vs. centerdistance")
        sns.relplot(x="centerdistance", y="price", data=df)
        plt.show()
        print("Scatter plot: sqftprice vs. centerdistance")
        sns.relplot(x="centerdistance", y="sqftprice", data=df)
        plt.show()
        print("Scatter plot: price vs. waterdistance")
        sns.relplot(x="waterdistance", y="price", data=df)
        plt.show()
        print("Scatter plot: sqftprice vs. waterdistance")
        sns.relplot(x="waterdistance", y="sqftprice", data=df)
        plt.show()

    # Correlation Heatmap (Pearson)
    print("\nCorrelation heatmap:")
    plt.figure(figsize=(20, 15))
    corr = df.select_dtypes(include='number').corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr.round(2), annot=True, mask=mask, cmap="RdBu_r")
    plt.show()

    # Pairplot for selected variables
    print("\nScatter/Pairs plot for selected variables:")
    # Remove any columns not present (e.g. lastknownchange)
    safe_columns = [col for col in columns_histogram if col in df.columns]
    sns.pairplot(df[safe_columns])
    plt.show()