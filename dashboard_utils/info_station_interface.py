import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from .info_station_functions import *


def info_station_interface(df):
    # Interface utilisateur pour les info par station
    st.subheader("")
    st.subheader("📍 Info par station")

    ref_station = st.selectbox("🚉 Station", sorted(df["Departure station"].unique()))

    # Filtrer les données pour la station sélectionnée
    station_data = df[df["Departure station"] == ref_station].copy()

    station_data["Années"] = station_data["year"].drop_duplicates()

    table_data = {
        "Année": list(range(2018, 2025)),
        "Nombre de trains prévu": [],
        "Nombre de retards": [],
        "Nombre d'annulations": [],
        "Moyenne des retards": [],
    }

    for year in range(2018, 2025):
        table_data["Nombre de trains prévu"].append(
            count_trains_by_year(station_data, year)
        )
        table_data["Nombre de retards"].append(count_delays_by_year(station_data, year))
        table_data["Nombre d'annulations"].append(
            count_cancellations_by_year(station_data, year)
        )
        table_data["Moyenne des retards"].append(get_mean_delayed(station_data, year))

    table_df = pd.DataFrame(table_data)

    # Définir l'année comme index
    table_df.set_index("Année", inplace=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.write("### Statistiques par année")
        st.dataframe(
            table_df,
            width=600,
            column_config={
                "Nombre de trains prévu": st.column_config.NumberColumn(
                    "Trains prévus", width=90, help="Nombre total de trains prévus"
                ),
                "Nombre de retards": st.column_config.NumberColumn(
                    "Retards", width=120, help="Nombre total de retards"
                ),
                "Nombre d'annulations": st.column_config.NumberColumn(
                    "Annulations", width=120, help="Nombre total d'annulations"
                ),
                "Retard moyen": st.column_config.NumberColumn(
                    "Moyenne des retards",
                    width=120,
                    help="La moyenne des retards",
                ),
            },
        )

    with col2:
        st.write("### Localisation")
        stations_coords = {
            "AIX EN PROVENCE TGV": [43.4552, 5.3170],
            "ANGERS SAINT LAUD": [47.4646, -0.5570],
            "LYON PART DIEU": [45.7563, 4.8594],
            "ANGOULEME": [45.6500, 0.1500],
            "ANNECY": [45.9013, 6.1164],
            "ARRAS": [50.2855, 2.7833],
            "AVIGNON TGV": [43.9219, 4.7858],
            "BARCELONA": [41.379167, 2.140278],
            "BELLEGARDE (AIN)": [46.1094, 5.8231],
            "BESANCON FRANCHE COMTE TGV": [47.3072, 5.9533],
            "BORDEAUX ST JEAN": [44.8266, -0.5559],
            "BREST": [48.387779, -4.480458],
            "CHAMBERY CHALLES LES EAUX": [45.569497722, 5.91832966],
            "DIJON VILLE": [47.3200, 5.0230],
            "DOUAI": [50.371769, 3.090532],
            "DUNKERQUE": [51.030513, 2.368604],
            "FRANCFORT": [50.1071, 8.6638],
            "GENEVE": [46.2100, 6.1425],
            "GRENOBLE": [45.1908, 5.7147],
            "ITALIE": [41.900833, 12.501944],
            "LA ROCHELLE VILLE": [46.152427, -1.145153],
            "LAUSANNE": [46.5160, 6.6296],
            "LAVAL": [48.0767, -0.7608],
            "LE CREUSOT MONTCEAU MONTCHANIN": [46.8050, 4.4786],
            "LE MANS": [47.989829374, 0.188499246],
            "LILLE": [50.636997452, 3.071833046],
            "MACON LOCHE": [46.2800, 4.8300],
            "MADRID": [40.4066, -3.6892],
            "MARNE LA VALLEE": [48.8720, 2.7769],
            "MARSEILLE ST CHARLES": [43.3020, 5.3811],
            "METZ": [49.1090, 6.1760],
            "MONTPELLIER": [43.6045, 3.8795],
            "MULHOUSE VILLE": [47.7486, 7.3428],
            "NANCY": [48.6921, 6.1844],
            "NANTES": [47.217, -1.542],
            "NICE VILLE": [43.7034, 7.2663],
            "NIMES": [43.8340, 4.3610],
            "PARIS EST": [48.8761, 2.3595],
            "PARIS LYON": [48.8443, 2.3730],
            "PARIS MONTPARNASSE": [48.8400, 2.3200],
            "PARIS NORD": [48.8809, 2.3553],
            "PARIS VAUGIRARD": [48.8380, 2.3150],
            "PERPIGNAN": [42.696236, 2.879456],
            "POITIERS": [46.5821, 0.3330],
            "QUIMPER": [47.994698, -4.092329],
            "REIMS": [49.2583, 4.0244],
            "RENNES": [48.1033, -1.6720],
            "SAINT ETIENNE CHATEAUCREUX": [45.443561, 4.399495],
            "ST MALO": [48.6470, -2.0030],
            "ST PIERRE DES CORPS": [47.3947, 0.7231],
            "STRASBOURG": [48.5846, 7.7366],
            "STUTTGART": [48.7833, 9.1833],
            "TOULON": [43.1242, 5.9280],
            "TOULOUSE MATABIAU": [43.6110, 1.4540],
            "TOURCOING": [50.7166, 3.1681],
            "TOURS": [47.3889, 0.6883],
            "VALENCE ALIXAN TGV": [44.9884, 4.9750],
            "VANNES": [47.665322, -2.752573],
            "ZURICH": [47.3782, 8.5402],
        }

        # Créer la carte centrée sur l'Europe
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=5)

        # Si la station sélectionnée est dans notre dictionnaire
        if ref_station in stations_coords:
            folium.Marker(
                stations_coords[ref_station],
                popup=ref_station,
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(m)

        folium_static(m)

    with col3:
        st.write("### Courbe du retard moyen par année")
        import plotly.express as px

        # Préparer les données pour l'animation
        df_anim = station_data.copy()
        df_anim = df_anim[df_anim["year"].between(2018, 2024)]
        if not df_anim.empty:
            df_anim_grouped = (
                df_anim.groupby("year")["Average delay of all trains at arrival"]
                .mean()
                .reset_index()
            )
            df_anim_grouped = df_anim_grouped[
                df_anim_grouped["year"].between(2018, 2024)
            ]
            # Pour chaque frame, afficher la courbe jusqu'à l'année courante
            df_anim_grouped["year_str"] = df_anim_grouped["year"].astype(str)
            df_anim_grouped = df_anim_grouped.sort_values("year")
            df_anim_grouped["frame"] = df_anim_grouped["year"]
            df_frames = []
            for y in df_anim_grouped["year"]:
                temp = df_anim_grouped[df_anim_grouped["year"] <= y].copy()
                temp["frame"] = str(y)
                df_frames.append(temp)
            df_anim_full = pd.concat(df_frames)
            fig = px.line(
                df_anim_full,
                x="year",
                y="Average delay of all trains at arrival",
                animation_frame="frame",
                labels={
                    "year": "Année",
                    "Average delay of all trains at arrival": "Retard moyen (min)",
                },
                title="Évolution du retard moyen par année (animation)",
                markers=True,
                range_y=[
                    0,
                    df_anim_grouped["Average delay of all trains at arrival"].max() + 5,
                ],
            )
            fig.update_traces(line_color="red")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Pas de données pour afficher l'animation.")
