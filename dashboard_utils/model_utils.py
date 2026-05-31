import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd


def prepare_data(df, features, target):
    df_model = df[features + [target]].dropna()
    X = pd.get_dummies(df_model[features])
    y = df_model[target]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    }
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        results[name] = {"rmse": rmse, "r2": r2}

    param_grid = {"n_estimators": [100, 200], "max_depth": [10, 20, None]}
    grid_search = GridSearchCV(
        RandomForestRegressor(random_state=42),
        param_grid,
        scoring="neg_mean_squared_error",
        cv=3,
        n_jobs=-1,
    )
    grid_search.fit(X_train, y_train)
    best_rf = grid_search.best_estimator_
    best_rf_pred = best_rf.predict(X_test)
    best_rf_rmse = np.sqrt(mean_squared_error(y_test, best_rf_pred))
    best_rf_r2 = r2_score(y_test, best_rf_pred)
    results["Best Random Forest (Tuned)"] = {"rmse": best_rf_rmse, "r2": best_rf_r2}
    return best_rf, results
