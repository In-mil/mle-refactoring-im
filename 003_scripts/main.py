from load_data import load_data
from clean_data import clean_data
from feature_engineering import engineer_features
from explore_data import explore_data
from split_data import split_data
from train_model import train_linear_regression, train_poly_regression, train_elasticnet_regression
from evaluate_model import evaluate_model, error_analysis, visualize_errors
from safe_model import save_model


kc_data = load_data("001_data/King_County_House_prices_dataset.csv")
kc_data_clean = clean_data(kc_data)
kc_data_feat = engineer_features(kc_data_clean)
explore_data(kc_data_feat)
X_train, X_test, y_train, y_test = split_data(kc_data_feat)

# Lineares Modell
lin_model = train_linear_regression(X_train, y_train)
adj_r2_lin = evaluate_model(lin_model, X_test, y_test)
dferror_lin = error_analysis(y_test, lin_model.predict(X_test), X_test)
visualize_errors(dferror_lin)
save_model(lin_model, "004_reports_and_images/lin_model.skops")

# Polynomial Regression
poly_transformer, poly_model = train_poly_regression(X_train, y_train, degree=2)
X_train_poly = poly_transformer.fit_transform(X_train)
X_test_poly = poly_transformer.transform(X_test)
adj_r2_poly = evaluate_model(poly_model, X_test_poly, y_test)
dferror_poly = error_analysis(y_test, poly_model.predict(X_test_poly), X_test)
visualize_errors(dferror_poly)
save_model(poly_model, "004_reports_and_images/poly_model.skops")

# ElasticNet Regression
elastic_model = train_elasticnet_regression(X_train_poly, y_train)
adj_r2_elastic = evaluate_model(elastic_model, X_test_poly, y_test)
dferror_elastic = error_analysis(y_test, elastic_model.predict(X_test_poly), X_test)
visualize_errors(dferror_elastic)
save_model(elastic_model, "004_reports_and_images/elasticnet_model.skops")