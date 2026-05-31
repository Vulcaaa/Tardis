import pandas as pd


def filter_data(df, dayofweek_filter, mois_filter, annee_filter=None):
    df_filtered = df.copy()
    if dayofweek_filter != -1:
        df_filtered = df_filtered[df_filtered["DayOfWeek"] == dayofweek_filter]
    if mois_filter != -1:
        df_filtered = df_filtered[df_filtered["Month"] == mois_filter]
    if annee_filter is not None:
        df_filtered = df_filtered[df_filtered["year"] == annee_filter]
    return df_filtered
