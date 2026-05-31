import pandas as pd
import streamlit as st


def load_user_csv(uploaded_file):
    """
    Charge et valide un fichier CSV uploadé par l'utilisateur.
    Retourne un DataFrame ou None si erreur.
    """
    try:
        df = pd.read_csv(uploaded_file)
        # Vérification : présence des colonnes brutes attendues
        required_columns = [
            "Departure station",
            "Arrival station",
            "Date",
            "Average delay of all trains at arrival",
        ]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Colonnes manquantes dans le fichier : {', '.join(missing)}")
            return None
        # Création des colonnes DayOfWeek, Hour, Month, year à partir de Date
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        if df["Date"].isnull().any():
            st.error(
                "Certaines valeurs de la colonne 'Date' sont invalides ou manquantes."
            )
            return None
        if "DayOfWeek" not in df.columns:
            df["DayOfWeek"] = df["Date"].dt.dayofweek
        if "Hour" not in df.columns:
            df["Hour"] = df["Date"].dt.hour
        if "Month" not in df.columns:
            df["Month"] = df["Date"].dt.month
        if "year" not in df.columns:
            df["year"] = df["Date"].dt.year
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None
