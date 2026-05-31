# TARDIS - Train Delay Prediction Dashboard

## 1. Approach

This project aims to predict the average delay of trains at arrival using historical SNCF data. The workflow is structured as follows:

- **Data Cleaning & Preparation:**
  - Raw train traffic data is cleaned to remove duplicates, handle missing values, and correct anomalies (see `tardis_eda.ipynb`).
  - Feature engineering extracts relevant columns (e.g., day of week, hour, year, month) from the date.
  - The cleaned dataset is saved as `cleaned_dataset.csv` for modeling and dashboard use.

- **Modeling:**
  - Several regression models (Linear Regression, Decision Tree, Random Forest) are trained to predict the average delay at arrival.
  - Hyperparameter tuning is performed for the Random Forest model.
  - Model performance is evaluated using RMSE and R² metrics (see `tardis_model.ipynb`).

- **Dashboard:**
  - An interactive Streamlit dashboard (`tardis_dashboard.py`) allows users to:
    - Upload their own CSV data (with required columns).
    - Filter data by year, month, and day of week.
    - Visualize delay distributions, heatmaps, and station statistics.
    - Train models and view prediction results.
    - Predict delays for custom scenarios.

## 2. Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Vulcaaa/Tardis.git
   cd Tardis
   ```

2. **Create and activate a virtual environment (recommended):**
   ```sh
   python3 -m venv myvenv
   source myvenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## 3. Usage

> **Note on data:** the SNCF dataset (`dataset.csv` / `cleaned_dataset.csv`) is **not included** in this repository. Provide your own CSV with the columns listed below (the original data comes from SNCF Open Data on monthly train regularity).

### A. Data Cleaning & Exploration
- Open and run `tardis_eda.ipynb` in Jupyter or VS Code to clean and explore the raw dataset (`dataset.csv`).
- The notebook will output a cleaned file: `cleaned_dataset.csv`.

### B. Model Training & Evaluation
- Open and run `tardis_model.ipynb` to train and evaluate regression models on the cleaned data.
- You can experiment with different features or models in this notebook.

### C. Launch the Dashboard
1. **Start the Streamlit dashboard:**
   ```sh
   streamlit run tardis_dashboard.py
   ```
2. **In your browser:**
   - Upload your own CSV file (must contain: `Departure station`, `Arrival station`, `Date`, `Average delay of all trains at arrival`).
   - Use the sidebar filters to explore and visualize the data.
   - View model results and make predictions interactively.

---

Tip:

Your CSV must contain the columns: <code>Departure station</code>, <code>Arrival station</code>, <code>Date</code>, <code>Average delay of all trains at arrival</code>.

All code is modularized in the <code>dashboard_utils/</code> folder for easy extension and maintenance.

Coding style: This project uses the <a href="https://github.com/astral-sh/ruff">ruff</a> formatter for Python code style and linting.

---

#### <span style="color: #1a73e8;">Made by Epitech Tek1 Student :</span>
- **COMBE--BRACCIALE Nielsen**
- **ABERKANE Mathys**
- **BERTRAND Teddy**