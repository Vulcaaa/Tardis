import streamlit as st
import pandas as pd


def prediction_interface(df, X_train, model):
    """Affiche l'interface utilisateur pour la prédiction du retard."""
    st.subheader("")
    st.subheader("🔍 Prédire un retard")
    departure = st.selectbox(
        "🚉 Station de départ", sorted(df["Departure station"].unique())
    )
    arrival = st.selectbox(
        "🏁 Station d'arrivée", sorted(df["Arrival station"].unique())
    )
    jours_semaine = {
        "Lundi": 0,
        "Mardi": 1,
        "Mercredi": 2,
        "Jeudi": 3,
        "Vendredi": 4,
        "Samedi": 5,
        "Dimanche": 6,
    }
    jour_choisi = st.radio(
        "📅 Jour de la semaine", list(jours_semaine.keys()), horizontal=True
    )
    dayofweek = jours_semaine[jour_choisi]
    heures = [f"{h:02d}:00" for h in range(24)]
    heure_str = st.selectbox("🕐 Heure de la journée", heures)
    hour = int(heure_str.split(":")[0])
    if st.button("Prédire le retard"):
        input_df = pd.DataFrame(
            [
                {
                    "Departure station": departure,
                    "Arrival station": arrival,
                    "DayOfWeek": dayofweek,
                    "Hour": hour,
                }
            ]
        )
        input_encoded = pd.get_dummies(input_df)
        missing_cols = set(X_train.columns) - set(input_encoded.columns)
        if missing_cols:
            missing_df = pd.DataFrame(
                0, index=input_encoded.index, columns=list(missing_cols)
            )
            input_encoded = pd.concat([input_encoded, missing_df], axis=1)
        input_encoded = input_encoded[X_train.columns]
        prediction = model.predict(input_encoded)[0]
        st.success(f"✅ Retard moyen estimé : {prediction:.2f} minutes")
