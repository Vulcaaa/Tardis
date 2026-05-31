import streamlit as st
from dashboard_utils.data_utils import filter_data
from dashboard_utils.model_utils import prepare_data, train_models
from dashboard_utils.dashboard_charts import show_charts
from dashboard_utils.user_filters import user_filters
from dashboard_utils.heatmap_utils import heatmap_utils
from dashboard_utils.prediction_interface import prediction_interface
from dashboard_utils.info_station_interface import info_station_interface
from dashboard_utils.summary_interface import summary_stats
from dashboard_utils.verif_file import load_user_csv


@st.cache_resource
def get_trained_model(X_train, X_test, y_train, y_test):
    return train_models(X_train, X_test, y_train, y_test)


def main():
    st.set_page_config(page_title="Prédiction des Retards de Trains", layout="wide")
    st.title("🚆 Prédiction du Retard Moyen des Trains à l'Arrivée")

    st.info("""
    **Colonnes attendues dans votre fichier CSV :**
    - Departure station
    - Arrival station
    - Date (format YYYY-MM-DD HH:MM:SS)
    - Average delay of all trains at arrival
    """)

    uploaded_file = st.file_uploader("Importer votre propre fichier CSV:", type=["csv"])
    if uploaded_file is None:
        st.stop()
    df = load_user_csv(uploaded_file)
    if df is None:
        st.stop()

    # Filtres
    (
        jour_selection,
        dayofweek_filter,
        mois_labels,
        mois_selection,
        mois_filter,
        annee_selection,
        annee_filter,
    ) = user_filters(df)
    # Filtrage sur jour / mois / année
    df_filtered = filter_data(df, dayofweek_filter, mois_filter, annee_filter)
    st.markdown(f"📊 Nombre de trajets filtrés : **{len(df_filtered)}**")

    # Heatmap
    heatmap_data = heatmap_utils(
        df_filtered, dayofweek_filter, mois_filter, mois_labels, jour_selection
    )
    st.subheader("📈 Distribution des Retards")
    show_charts(
        df_filtered,
        heatmap_data,
        annee_selection=annee_selection,
        mois_filter=mois_filter,
    )

    info_station_interface(df)
    summary_stats(df)
    # Modélisation & Prédiction
    if len(df) < 2:
        st.warning(
            "Pas assez de données pour entraîner et tester un modèle (au moins 2 lignes requises après filtrage). Veuillez élargir vos filtres."
        )
    else:
        features = ["Departure station", "Arrival station", "DayOfWeek", "Hour"]
        target = "Average delay of all trains at arrival"
        X_train, X_test, y_train, y_test = prepare_data(df, features, target)
        model, results = get_trained_model(X_train, X_test, y_train, y_test)
        st.subheader("")
        st.subheader("📊 Résultats des modèles")
        for name, res in results.items():
            st.markdown(f"**{name}** | RMSE: {res['rmse']:.2f} | R²: {res['r2']:.2f}")
        with st.expander("ℹ️ Que signifient ces chiffres ?"):
            st.markdown("""
            - **Erreur moyenne estimée (RMSE)** : Plus ce chiffre est bas, plus la prédiction est précise.
            - **Qualité de la prédiction (R²)** : Se situe entre 0 et 1. Plus proche de 1 = meilleure qualité de prédiction.
            """)
        prediction_interface(df, X_train, model)


if __name__ == "__main__":
    main()
