import pandas as pd
import pytest
from dashboard_utils.data_utils import filter_data
from dashboard_utils.verif_file import load_user_csv
from io import StringIO
import numpy as np
from dashboard_utils.model_utils import prepare_data, train_models
from dashboard_utils.heatmap_utils import heatmap_utils
from dashboard_utils.info_station_functions import (
    count_trains_by_year,
    count_delays_by_year,
    count_cancellations_by_year,
    get_mean_delayed,
)


def test_filter_data():
    df = pd.DataFrame(
        {
            "DayOfWeek": [0, 1, 2],
            "Month": [1, 2, 3],
            "year": [2022, 2023, 2022],
            "val": [10, 20, 30],
        }
    )
    # Test dayofweek filter
    filtered = filter_data(df, 1, -1)
    assert len(filtered) == 1
    assert filtered.iloc[0]["DayOfWeek"] == 1
    # Test month filter
    filtered = filter_data(df, -1, 3)
    assert len(filtered) == 1
    assert filtered.iloc[0]["Month"] == 3
    # Test year filter
    filtered = filter_data(df, -1, -1, 2022)
    assert len(filtered) == 2
    assert all(filtered["year"] == 2022)


def test_load_user_csv_valid():
    csv = StringIO(
        """Departure station,Arrival station,Date,Average delay of all trains at arrival\nA,B,2023-01-01 10:00:00,5\nC,D,2023-01-02 12:00:00,10\n"""
    )
    df = load_user_csv(csv)
    assert df is not None
    assert "DayOfWeek" in df.columns
    assert "Hour" in df.columns
    assert "Month" in df.columns
    assert "year" in df.columns
    assert len(df) == 2


def test_load_user_csv_missing_column():
    csv = StringIO(
        """Departure station,Arrival station,Date\nA,B,2023-01-01 10:00:00\n"""
    )
    df = load_user_csv(csv)
    assert df is None


def test_prepare_data():
    df = pd.DataFrame(
        {
            "Departure station": ["A", "B", "A", "B"],
            "Arrival station": ["C", "C", "D", "D"],
            "DayOfWeek": [0, 1, 2, 3],
            "Hour": [10, 12, 14, 16],
            "Average delay of all trains at arrival": [5, 10, 15, 20],
        }
    )
    features = ["Departure station", "Arrival station", "DayOfWeek", "Hour"]
    target = "Average delay of all trains at arrival"
    X_train, X_test, y_train, y_test = prepare_data(df, features, target)
    assert X_train.shape[0] + X_test.shape[0] == 4
    assert y_train.shape[0] + y_test.shape[0] == 4
    assert set(X_train.columns) == set(X_test.columns)


def test_train_models():
    df = pd.DataFrame(
        {
            "Departure station": ["A", "B", "A", "B", "A", "B", "A", "B"],
            "Arrival station": ["C", "C", "D", "D", "C", "C", "D", "D"],
            "DayOfWeek": [0, 1, 2, 3, 0, 1, 2, 3],
            "Hour": [10, 12, 14, 16, 10, 12, 14, 16],
            "Average delay of all trains at arrival": [5, 10, 15, 20, 6, 11, 16, 21],
        }
    )
    features = ["Departure station", "Arrival station", "DayOfWeek", "Hour"]
    target = "Average delay of all trains at arrival"
    X_train, X_test, y_train, y_test = prepare_data(df, features, target)
    model, results = train_models(X_train, X_test, y_train, y_test)
    assert hasattr(model, "predict")
    assert "Linear Regression" in results
    assert "Decision Tree" in results
    assert "Random Forest" in results
    assert "Best Random Forest (Tuned)" in results
    for res in results.values():
        assert "rmse" in res and "r2" in res


def test_heatmap_utils():
    df = pd.DataFrame(
        {
            "DayOfWeek": [0, 1, 2, 0, 1, 2],
            "Month": [1, 1, 1, 2, 2, 2],
            "Average delay of all trains at arrival": [5, 10, 15, 20, 25, 30],
        }
    )
    mois_labels = ["Tous", "Janvier", "Février", "Mars"]
    # Test with dayofweek_filter
    heatmap = heatmap_utils(df, 1, -1, mois_labels, "Mardi")
    assert not heatmap.empty
    # Test with mois_filter
    heatmap = heatmap_utils(df, -1, 2, mois_labels, "Lundi")
    assert not heatmap.empty


def test_info_station_functions():
    df = pd.DataFrame(
        {
            "year": [2022, 2022, 2023],
            "Number of scheduled trains": [10, 20, 30],
            "Number of trains delayed at departure": [1, 2, 3],
            "Number of cancelled trains": [0, 1, 0],
            "Average delay of late trains at departure": [5, 10, 15],
        }
    )
    assert count_trains_by_year(df, 2022) == 30
    assert count_delays_by_year(df, 2022) == 3
    assert count_cancellations_by_year(df, 2022) == 1
    assert get_mean_delayed(df, 2022) == 7.5
