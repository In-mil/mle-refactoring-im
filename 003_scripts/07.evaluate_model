def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    """
    Evaluates a regression model using R².

    Args:
        model: Trained regression model.
        X_test (pd.DataFrame): Test feature matrix.
        y_test (pd.Series): Test target vector.

    Returns:
        float: Adjusted R² score.
    """
    y_pred = model.predict(X_test)
    n, k = X_test.shape
    r2 = r2_score(y_test, y_pred)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    print(f"Adjusted R²: {adj_r2:.2f}")
    return adj_r2

def error_analysis(y_true: pd.Series, y_pred: np.ndarray, X_test: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with prediction errors.

    Args:
        y_true (pd.Series): True target values.
        y_pred (np.ndarray): Predicted target values.
        X_test (pd.DataFrame): Test features (must contain 'lat', 'long', 'id').

    Returns:
        pd.DataFrame: DataFrame with errors.
    """
    df = pd.DataFrame({
        "price": y_true,
        "price_prediction": np.round(y_pred, 2),
        "pricedifference": np.round(y_pred - y_true, 2),
        "pricedifference_percent": np.round((y_pred - y_true) / y_true * 100, 2),
        "latitude": X_test['lat'].values,
        "longitude": X_test['long'].values,
        "id": X_test['id'].values
    })
    df.reset_index(drop=True, inplace=True)
    print(df.head(2))
    return df