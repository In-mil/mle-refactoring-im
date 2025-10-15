from 01.load_data import load_data
from 02.clean_data import clean_data
from 03.feature_engineering import engineer_features
from 04.explore_data import explore_data
from 05.split_data import split_data
from 06.train_model import train_linear_regression, train_poly_regression, train_elasticnet_regression
from 07.evaluate_model import evaluate_model
from 08.safe_model import save_model

# Dann die Aufrufkommandos wie in deiner Liste!
kc_data = load_data("001_data/King_County_House_prices_dataset.csv")
kc_data_clean = clean_data(kc_data)
kc_data_feat = engineer_features(kc_data_clean)
explore_data(kc_data_feat)
X_train, X_test, y_train, y_test = split_data(kc_data_feat)
lin_model = train_linear_regression(X_train, y_train)
poly_transformer, poly_model = train_poly_regression(X_train, y_train, degree=2)
X_train_poly = poly_transformer.fit_transform(X_train)
X_test_poly = poly_transformer.transform(X_test)
elastic_model = train_elasticnet_regression(X_train_poly, y_train)
evaluate_model(lin_model, X_test, y_test)
evaluate_model(poly_model, X_test_poly, y_test)
evaluate_model(elastic_model, X_test_poly, y_test)
save_model(lin_model, "004_reports_and_images/lin_model.skops")
save_model(poly_model, "004_reports_and_images/poly_model.skops")
save_model(elastic_model, "004_reports_and_images/elasticnet_model.skops")
