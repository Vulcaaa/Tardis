import streamlit as st


def user_filters(df):
    """Affiche les filtres Streamlit et retourne les valeurs sélectionnées."""
    jours_semaine = {
        "Tous": -1,
        "Lundi": 0,
        "Mardi": 1,
        "Mercredi": 2,
        "Jeudi": 3,
        "Vendredi": 4,
        "Samedi": 5,
        "Dimanche": 6,
    }
    jour_selection = st.selectbox("📅 Jour de la semaine", list(jours_semaine.keys()))
    dayofweek_filter = jours_semaine[jour_selection]

    mois_labels = ["Tous"] + [
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
    mois_selection = st.selectbox("📆 Mois de l'année", mois_labels)
    mois_filter = -1 if mois_selection == "Tous" else mois_labels.index(mois_selection)

    if "year" in df.columns:
        annees_disponibles = sorted(df["year"].dropna().unique())
        annee_selection = st.selectbox(
            "📅 Année", ["Toutes"] + [str(int(a)) for a in annees_disponibles]
        )
        if annee_selection != "Toutes":
            annee_filter = int(annee_selection)
        else:
            annee_filter = None
    else:
        annee_selection = None
        annee_filter = None

    return (
        jour_selection,
        dayofweek_filter,
        mois_labels,
        mois_selection,
        mois_filter,
        annee_selection,
        annee_filter,
    )
