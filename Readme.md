# TARDIS

A train delay prediction project in **Python**: it predicts the average arrival delay of trains from historical **SNCF** data, and ships an interactive **Streamlit** dashboard to explore the data and run predictions.

## Features

- **Data cleaning & feature engineering** — duplicates, missing values and anomalies are handled, and features (day of week, hour, month, year) are extracted from the raw SNCF data (`tardis_eda.ipynb`)
- **Regression models** — Linear Regression, Decision Tree and Random Forest (with hyperparameter tuning), evaluated with RMSE and R² (`tardis_model.ipynb`)
- **Interactive dashboard** (`tardis_dashboard.py`) — upload a CSV, filter by year/month/day of week, visualize delay distributions, heatmaps and station statistics (folium maps), train models and predict custom scenarios
- **Modular code** — reusable helpers in `dashboard_utils/`, with tests in `test_dashboard_utils.py`

## Build

Requires Python 3 and the listed dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. **Clean & explore the data** — run `tardis_eda.ipynb` (outputs a cleaned dataset).
2. **Train & evaluate models** — run `tardis_model.ipynb`.
3. **Launch the dashboard:**

```bash
streamlit run tardis_dashboard.py
```

In the browser, upload a CSV containing `Departure station`, `Arrival station`, `Date` and `Average delay of all trains at arrival`, then filter, visualize and predict.

> The SNCF dataset is not included — provide your own CSV (original data: SNCF Open Data, monthly train regularity).

## Credits

Team project realized as part of the Epitech curriculum — **Artificial Intelligence** module.

- Nielsen Combe-Bracciale
- Mathys Aberkane
- Teddy Bertrand
