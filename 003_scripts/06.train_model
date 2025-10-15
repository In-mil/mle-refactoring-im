from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd

def train_linear_regression(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """
    Trains a simple linear regression model.

    Args:
        X_train (pd.DataFrame): Training feature matrix.
        y_train (pd.Series): Training target vector.

    Returns:
        LinearRegression: Trained linear regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_poly_regression(X_train: pd.DataFrame, y_train: pd.Series, degree: int = 2) -> tuple:
    """
    Trains a polynomial regression model.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target.
        degree (int): Degree of polynomial features, default 2.

    Returns:
        tuple: (PolynomialFeatures transformer, trained LinearRegression model)
    """
    poly = PolynomialFeatures(degree)
    X_train_poly = poly.fit_transform(X_train)
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    return poly, model

def train_elasticnet_regression(X_train: pd.DataFrame, y_train: pd.Series) -> ElasticNet:
    """
    Trains an ElasticNet regression model with grid search.

    Args:
        X_train (pd.DataFrame): Training features (polynomial if needed).
        y_train (pd.Series): Training target.

    Returns:
        ElasticNet: Trained model with best found parameters.
    """
    param_grid = {
        "alpha": [0.1, 0.5, 1, 5, 10],
        "l1_ratio": [1, 0.5, 0]
    }
    enet = ElasticNet(max_iter=50000, tol=0.2)
    grid = GridSearchCV(enet, param_grid, cv=5, verbose=1, n_jobs=-1)
    grid.fit(X_train, y_train)
    print("Best ElasticNet params:", grid.best_params_)
    model = ElasticNet(max_iter=50000, tol=0.2, **grid.best_params_)
    model.fit(X_train, y_train)
    return model