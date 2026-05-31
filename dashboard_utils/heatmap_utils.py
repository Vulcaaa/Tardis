import pandas as pd


def heatmap_utils(df, dayofweek_filter, mois_filter, mois_labels, jour_selection):
    """Prépare les données pour la heatmap selon les filtres."""
    if mois_filter != -1:
        heatmap_df = df[df["Month"] == mois_filter]
    else:
        heatmap_df = df

    if dayofweek_filter != -1:
        heatmap_df = heatmap_df[heatmap_df["DayOfWeek"] == dayofweek_filter]
        heatmap_data = (
            heatmap_df.groupby(["Month"])["Average delay of all trains at arrival"]
            .mean()
            .to_frame()
            .T
        )
        heatmap_data.columns = [mois_labels[m] for m in heatmap_data.columns]
        heatmap_data.index = [jour_selection]
    else:
        heatmap_data = (
            heatmap_df.groupby(["DayOfWeek", "Month"])[
                "Average delay of all trains at arrival"
            ]
            .mean()
            .unstack()
        )
        heatmap_data.columns = [mois_labels[m] for m in heatmap_data.columns]
        jours_labels = [
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche",
        ]
        heatmap_data.index = [jours_labels[d] for d in heatmap_data.index]
    return heatmap_data
