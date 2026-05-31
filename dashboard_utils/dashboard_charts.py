import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.colors as mcolors


def show_charts(df_filtered, heatmap_data, annee_selection=None, mois_filter=None):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Histogramme du retard moyen à l'arrivée")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            fig_hist_small, ax_hist_small = plt.subplots(figsize=(4, 2))
            sns.histplot(
                df_filtered["Average delay of all trains at arrival"],
                bins=30,
                kde=True,
                ax=ax_hist_small,
                color="skyblue",
            )
            ax_hist_small.set_title("Distribution du retard moyen à l'arrivée")
            ax_hist_small.set_xlabel("Retard moyen à l'arrivée (minutes)")
            ax_hist_small.set_ylabel("Nombre de trajets")
            st.pyplot(fig_hist_small)
            plt.close(fig_hist_small)

        # Chart : nombre de trains en retard selon année/mois
        st.markdown("#### Nombre de trains en retard")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            # Définir un train en retard : delay à l'arrivée > 0
            df_late = df_filtered[
                df_filtered["Average delay of all trains at arrival"] > 0
            ]
            # Cas 1 : année spécifiée (pas 'Toutes')
            if annee_selection is not None and annee_selection != "Toutes":
                if "month" in df_late.columns:
                    group = df_late.groupby(["month"]).size()
                    mois_labels = [
                        "Janvier",
                        "Février",
                        "Mars",
                        "Avril",
                        "Mai",
                        "Juin",
                        "Juillet",
                        "Août",
                        "Septembre",
                        "Octobre",
                        "Novembre",
                        "Décembre",
                    ]
                    group = group.reindex(range(1, 13), fill_value=0)
                    fig, ax = plt.subplots(figsize=(7, 2.5))
                    x = list(range(1, 13))
                    y = group.values
                    ax.plot(x, y, marker="o", color="orangered", linestyle="-")
                    for i, val in enumerate(y):
                        ax.scatter(x[i], val, color="orangered")
                    ax.set_xticks(x)
                    ax.set_xticklabels([mois_labels[m - 1] for m in x], rotation=45)
                    ax.set_title(
                        f"Nombre de trains en retard par mois ({annee_selection})"
                    )
                    ax.set_xlabel("Mois")
                    ax.set_ylabel("Nombre de trains en retard")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info(f"Colonnes présentes : {list(df_late.columns)}")
                    st.info("Colonne 'month' absente des données.")
            # Cas 2 : rien de spécifié (Toutes les années, tous les mois)
            elif (annee_selection is None or annee_selection == "Toutes") and (
                mois_filter is None or mois_filter == -1
            ):
                if "year" in df_late.columns and "month" in df_late.columns:
                    group = df_late.groupby(["year"]).size()
                    x = group.index.astype(str)
                    y = group.values
                    fig, ax = plt.subplots(figsize=(7, 2.5))
                    ax.plot(x, y, marker="o", color="royalblue", linestyle="-")
                    for i, val in enumerate(y):
                        ax.scatter(x[i], val, color="royalblue")
                    ax.set_title("Nombre de trains en retard par année")
                    ax.set_xlabel("Année")
                    ax.set_ylabel("Nombre de trains en retard")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info(f"Colonnes présentes : {list(df_late.columns)}")
                    st.info("Colonnes 'year' ou 'month' absentes des données.")
            # Cas 3 : un mois spécifié (mais pas d'année)
            elif (annee_selection is None or annee_selection == "Toutes") and (
                mois_filter is not None and mois_filter != -1
            ):
                if "year" in df_late.columns and "month" in df_late.columns:
                    df_month = df_late[df_late["month"] == mois_filter]
                    group = df_month.groupby(["year"]).size()
                    x = group.index.astype(str)
                    y = group.values
                    fig, ax = plt.subplots(figsize=(7, 2.5))
                    ax.plot(x, y, marker="o", color="coral", linestyle="-")
                    for i, val in enumerate(y):
                        ax.scatter(x[i], val, color="coral")
                    ax.set_title(
                        f"Nombre de trains en retard par année (mois={mois_filter})"
                    )
                    ax.set_xlabel("Année")
                    ax.set_ylabel("Nombre de trains en retard")
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info(f"Colonnes présentes : {list(df_late.columns)}")
                    st.info("Colonnes 'year' ou 'month' absentes des données.")

    with col2:
        st.markdown("#### Boxplot du retard moyen à l'arrivée")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            fig_box_small, ax_box_small = plt.subplots(figsize=(4, 1.5))
            sns.boxplot(
                x=df_filtered["Average delay of all trains at arrival"],
                ax=ax_box_small,
                color="lightcoral",
            )
            ax_box_small.set_title("Répartition du retard moyen à l'arrivée")
            ax_box_small.set_xlabel("Retard moyen à l'arrivée (minutes)")
            ax_box_small.set_ylabel("")
            st.pyplot(fig_box_small)
            plt.close(fig_box_small)

        # Barplot en row2 de col2 : nombre de trajets par tranche de retard
        st.markdown("#### Nombre de trajets par tranche de retard")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            max_delay = df_filtered["Average delay of all trains at arrival"].max()
            if max_delay <= 0 or pd.isna(max_delay):
                st.info(
                    "Impossible de créer des tranches de retard : aucune valeur positive."
                )
            else:
                bins = [0, 5, 10, 15, 20, 30, 60]
                if max_delay > 120:
                    bins.append(max_delay + 1)
                    labels = [
                        "0-5",
                        "5-10",
                        "10-15",
                        "15-20",
                        "20-30",
                        "30-60",
                        f"60-{int(max_delay)}",
                    ]
                else:
                    bins.append(max_delay + 1)
                    labels = ["0-5", "5-10", "10-15", "15-20", "20-30", "30-60", ">60"]
                # S'assurer que bins est strictement croissant
                bins = sorted(list(set(bins)))
                df_filtered = df_filtered.copy()
                df_filtered["delay_bin"] = pd.cut(
                    df_filtered["Average delay of all trains at arrival"],
                    bins=bins,
                    labels=labels[: len(bins) - 1],
                    right=False,
                    include_lowest=True,
                )
                delay_counts = df_filtered["delay_bin"].value_counts().sort_index()
                fig_bar, ax_bar = plt.subplots(figsize=(4, 2))
                sns.barplot(
                    x=delay_counts.index,
                    y=delay_counts.values,
                    ax=ax_bar,
                    color="mediumseagreen",
                )
                ax_bar.set_title("Nombre de trajets par tranche de retard (min)")
                ax_bar.set_xlabel("Tranche de retard (minutes)")
                ax_bar.set_ylabel("Nombre de trajets")
                st.pyplot(fig_bar)
                plt.close(fig_bar)

    with col3:
        st.markdown("#### Heatmap Retard")
        if heatmap_data.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            fig_heat, ax_heat = plt.subplots(figsize=(5, 3))
            sns.heatmap(
                heatmap_data,
                cmap="Reds",
                linewidths=0.3,
                linecolor="white",
                ax=ax_heat,
                annot=True,
                fmt=".1f",
            )
            ax_heat.set_title("Retard moyen (min) par jour et mois")
            ax_heat.set_xlabel("Mois")
            ax_heat.set_ylabel("Jour")
            st.pyplot(fig_heat)
            plt.close(fig_heat)

        # Barplot : top 10 retard moyen par gare de départ (déplacé ici)
        st.markdown("#### Top 10 retard moyen par gare de départ")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            delay_by_station = (
                df_filtered.groupby("Departure station")[
                    "Average delay of all trains at arrival"
                ]
                .mean()
                .sort_values(ascending=False)
            )
            delay_by_station_top10 = delay_by_station.head(10)
            palette = sns.color_palette("Reds", n_colors=len(delay_by_station_top10))
            palette.reverse()
            fig_bar, ax_bar = plt.subplots(figsize=(4, 2))
            sns.barplot(
                x=delay_by_station_top10.values,
                y=delay_by_station_top10.index,
                ax=ax_bar,
                hue=delay_by_station_top10.index,
                palette=palette,
                legend=False,
            )
            ax_bar.set_title("Top 10 retard moyen par gare de départ")
            ax_bar.set_xlabel("Retard moyen (minutes)")
            ax_bar.set_ylabel("Gare de départ")
            st.pyplot(fig_bar)
            plt.close(fig_bar)

    with st.expander("🔍 Voir les graphiques en grand format"):
        # Heatmap Corrélation des facteurs de retard
        st.markdown("#### Heatmap Corrélation des facteurs de retard")
        # Sélection des colonnes de facteurs de retard
        delay_factor_cols = [
            col for col in df_filtered.columns if col.startswith("Pct delay due to ")
        ]
        if len(delay_factor_cols) >= 2:
            corr = df_filtered[delay_factor_cols].corr()
            fig_corr, ax_corr = plt.subplots(figsize=(5, 3))
            sns.heatmap(
                corr, cmap="coolwarm", annot=True, fmt=".2f", ax=ax_corr, cbar=True
            )
            ax_corr.set_title("Corrélation entre facteurs de retard (%)")
            st.pyplot(fig_corr)
            plt.close(fig_corr)
        else:
            st.info(
                "Pas assez de colonnes de facteurs de retard pour afficher une heatmap de corrélation."
            )
        # Histogramme grand format
        st.markdown("### Histogramme du retard moyen à l'arrivée (grand format)")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            fig_hist_big, ax_hist_big = plt.subplots(figsize=(8, 4))
            sns.histplot(
                df_filtered["Average delay of all trains at arrival"],
                bins=30,
                kde=True,
                ax=ax_hist_big,
                color="skyblue",
            )
            ax_hist_big.set_title("Distribution du retard moyen à l'arrivée")
            ax_hist_big.set_xlabel("Retard moyen à l'arrivée (minutes)")
            ax_hist_big.set_ylabel("Nombre de trajets")
            st.pyplot(fig_hist_big)
            plt.close(fig_hist_big)

        # Barplot top 10 gares grand format
        st.markdown("### Top 10 retard moyen par gare de départ (grand format)")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            delay_by_station = (
                df_filtered.groupby("Departure station")[
                    "Average delay of all trains at arrival"
                ]
                .mean()
                .sort_values(ascending=False)
            )
            delay_by_station_top10 = delay_by_station.head(10)
            palette = sns.color_palette("Reds", n_colors=len(delay_by_station_top10))
            palette.reverse()
            fig_bar_top10_big, ax_bar_top10_big = plt.subplots(figsize=(8, 4))
            sns.barplot(
                x=delay_by_station_top10.values,
                y=delay_by_station_top10.index,
                ax=ax_bar_top10_big,
                hue=delay_by_station_top10.index,
                palette=palette,
                legend=False,
            )
            ax_bar_top10_big.set_title("Top 10 retard moyen par gare de départ")
            ax_bar_top10_big.set_xlabel("Retard moyen (minutes)")
            ax_bar_top10_big.set_ylabel("Gare de départ")
            st.pyplot(fig_bar_top10_big)
            plt.close(fig_bar_top10_big)

        # Boxplot grand format
        st.markdown("### Boxplot du retard moyen à l'arrivée (grand format)")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            fig_box_big, ax_box_big = plt.subplots(figsize=(8, 2))
            sns.boxplot(
                x=df_filtered["Average delay of all trains at arrival"],
                ax=ax_box_big,
                color="lightcoral",
            )
            ax_box_big.set_title("Répartition du retard moyen à l'arrivée")
            ax_box_big.set_xlabel("Retard moyen à l'arrivée (minutes)")
            ax_box_big.set_ylabel("")
            st.pyplot(fig_box_big)
            plt.close(fig_box_big)

        # Barplot nombre de trajets par tranche de retard grand format
        st.markdown("### Nombre de trajets par tranche de retard (grand format)")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            max_delay = df_filtered["Average delay of all trains at arrival"].max()
            if max_delay > 0 and not pd.isna(max_delay):
                bins = [0, 5, 10, 15, 20, 30, 60]
                if max_delay > 60:
                    bins.append(max_delay + 1)
                    labels = [
                        "0-5",
                        "5-10",
                        "10-15",
                        "15-20",
                        "20-30",
                        "30-60",
                        f"60-{int(max_delay)}",
                    ]
                else:
                    bins.append(max_delay + 1)
                    labels = ["0-5", "5-10", "10-15", "15-20", "20-30", "30-60", ">60"]
                bins = sorted(list(set(bins)))
                df_filtered_exp = df_filtered.copy()
                df_filtered_exp["delay_bin"] = pd.cut(
                    df_filtered_exp["Average delay of all trains at arrival"],
                    bins=bins,
                    labels=labels[: len(bins) - 1],
                    right=False,
                    include_lowest=True,
                )
                delay_counts = df_filtered_exp["delay_bin"].value_counts().sort_index()
                fig_bar_delay_big, ax_bar_delay_big = plt.subplots(figsize=(8, 3))
                sns.barplot(
                    x=delay_counts.index,
                    y=delay_counts.values,
                    ax=ax_bar_delay_big,
                    color="mediumseagreen",
                )
                ax_bar_delay_big.set_title(
                    "Nombre de trajets par tranche de retard (min)"
                )
                ax_bar_delay_big.set_xlabel("Tranche de retard (minutes)")
                ax_bar_delay_big.set_ylabel("Nombre de trajets")
                st.pyplot(fig_bar_delay_big)
                plt.close(fig_bar_delay_big)
            else:
                st.info(
                    "Impossible de créer des tranches de retard : aucune valeur positive."
                )

        # Heatmap grand format
        st.markdown("#### Heatmap complet")
        if heatmap_data.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            fig_heat_big, ax_heat_big = plt.subplots(figsize=(8, 5))
            sns.heatmap(
                heatmap_data,
                cmap="Reds",
                linewidths=0.3,
                linecolor="white",
                ax=ax_heat_big,
                annot=True,
                fmt=".1f",
            )
            ax_heat_big.set_title("Retard moyen (min) par jour et mois")
            ax_heat_big.set_xlabel("Mois")
            ax_heat_big.set_ylabel("Jour")
            st.pyplot(fig_heat_big)
            plt.close(fig_heat_big)

        # Courbe du nombre de trains en retard grand format
        st.markdown("### Nombre de trains en retard (grand format)")
        if df_filtered.empty:
            st.info("Aucune donnée disponible pour ce filtre.")
        else:
            df_late = df_filtered[
                df_filtered["Average delay of all trains at arrival"] > 0
            ]
            # Cas 1 : année spécifiée (pas 'Toutes')
            if annee_selection is not None and annee_selection != "Toutes":
                if "month" in df_late.columns:
                    group = df_late.groupby(["month"]).size()
                    mois_labels = [
                        "Janvier",
                        "Février",
                        "Mars",
                        "Avril",
                        "Mai",
                        "Juin",
                        "Juillet",
                        "Août",
                        "Septembre",
                        "Octobre",
                        "Novembre",
                        "Décembre",
                    ]
                    group = group.reindex(range(1, 13), fill_value=0)
                    fig_late_big, ax_late_big = plt.subplots(figsize=(10, 3))
                    x = list(range(1, 13))
                    y = group.values
                    ax_late_big.plot(x, y, marker="o", color="orangered", linestyle="-")
                    for i, val in enumerate(y):
                        ax_late_big.scatter(x[i], val, color="orangered")
                    ax_late_big.set_xticks(x)
                    ax_late_big.set_xticklabels(
                        [mois_labels[m - 1] for m in x], rotation=45
                    )
                    ax_late_big.set_title(
                        f"Nombre de trains en retard par mois ({annee_selection})"
                    )
                    ax_late_big.set_xlabel("Mois")
                    ax_late_big.set_ylabel("Nombre de trains en retard")
                    st.pyplot(fig_late_big)
                    plt.close(fig_late_big)
            # Cas 2 : rien de spécifié (Toutes les années, tous les mois)
            elif (annee_selection is None or annee_selection == "Toutes") and (
                mois_filter is None or mois_filter == -1
            ):
                if "year" in df_late.columns and "month" in df_late.columns:
                    group = df_late.groupby(["year"]).size()
                    x = group.index.astype(str)
                    y = group.values
                    fig_late_big, ax_late_big = plt.subplots(figsize=(10, 3))
                    ax_late_big.plot(x, y, marker="o", color="royalblue", linestyle="-")
                    for i, val in enumerate(y):
                        ax_late_big.scatter(x[i], val, color="royalblue")
                    ax_late_big.set_title("Nombre de trains en retard par année")
                    ax_late_big.set_xlabel("Année")
                    ax_late_big.set_ylabel("Nombre de trains en retard")
                    st.pyplot(fig_late_big)
                    plt.close(fig_late_big)
            # Cas 3 : un mois spécifié (mais pas d'année)
            elif (annee_selection is None or annee_selection == "Toutes") and (
                mois_filter is not None and mois_filter != -1
            ):
                if "year" in df_late.columns and "month" in df_late.columns:
                    df_month = df_late[df_late["month"] == mois_filter]
                    group = df_month.groupby(["year"]).size()
                    x = group.index.astype(str)
                    y = group.values
                    fig_late_big, ax_late_big = plt.subplots(figsize=(10, 3))
                    ax_late_big.plot(x, y, marker="o", color="coral", linestyle="-")
                    for i, val in enumerate(y):
                        ax_late_big.scatter(x[i], val, color="coral")
                    ax_late_big.set_title(
                        f"Nombre de trains en retard par année (mois={mois_filter})"
                    )
                    ax_late_big.set_xlabel("Année")
                    ax_late_big.set_ylabel("Nombre de trains en retard")
                    st.pyplot(fig_late_big)
                    plt.close(fig_late_big)
