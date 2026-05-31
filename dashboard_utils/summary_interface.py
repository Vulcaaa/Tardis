import streamlit as st
import pandas as pd


# dans mes fonctions utils : je return la somme quand je count le nb d'occ. je fois faire len plustot ?
def summary_stats(df):
    # Interface utilisateur pour les summary stats
    st.subheader("")
    st.subheader("🌎 Résumé statistiques")

    stations = df["Departure station"].drop_duplicates().tolist()

    table_data = {
        "Metrics": [
            "Nombre de trains prévu",
            "Taux de ponctualité (%)",
            "Nombre de retards",
            "Moyenne des retards",
            "Nombre d'annulations",
            "Nombre de dessertes",
        ],
    }

    # Ajouter une colonne pour chaque station
    for station in stations:
        station_data = df[df["Departure station"] == station]

        # Calculer les statistiques pour chaque station
        nb_trains = station_data["Number of scheduled trains"].sum()
        nb_delays = station_data["Number of trains delayed at departure"].sum()
        nb_cancellations = station_data["Number of cancelled trains"].sum()
        mean_delay = round(
            station_data["Average delay of late trains at departure"].mean(), 2
        )
        ontime_rate = round(
            ((nb_trains - (nb_delays + nb_cancellations)) * 100) / nb_trains, 2
        )
        nb_dessertes = len(station_data["Arrival station"])

        # Ajouter les données de la station comme nouvelle colonne
        table_data[station] = [
            nb_trains,
            ontime_rate,
            nb_delays,
            mean_delay,
            nb_cancellations,
            nb_dessertes,
        ]

    # Créer et afficher le DataFrame
    df_table = pd.DataFrame(table_data).set_index("Metrics")
    st.dataframe(df_table)
    # st.write("Voici le DataFrame brut :")
    # st.dataframe(df)
    return 0
