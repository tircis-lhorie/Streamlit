# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from streamlit_extras.switch_page_button import switch_page


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.sidebar.image("image/logo.png", use_container_width=True)

# --- Liste des PIN autorisés ---
AUTHORIZED_PINS = {"1234", "5678"}  # à adapter

# --- Session pour savoir si l'utilisateur est authentifié ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("🔐 Connexion requise")
    pin = st.text_input("Entrez votre code PIN à 4 chiffres", type="password", max_chars=4)
    if st.button("Se connecter"):
        if pin in AUTHORIZED_PINS:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code PIN incorrect.")

if not st.session_state.authenticated:
    login()
    st.stop()




st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")

# Espacement
st.markdown("## ")

# Affichage des 3 cartes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔗 Visualise les causalités")
    st.markdown("Carte interactive des liens entre KPIs.")
    if st.button("Accéder", key="go_graphe"):
        switch_page("Graphe")

with col2:
    st.markdown("### 📊 Découvre ton tableau de bord")
    st.markdown("Analyse l'évolution d’un indicateur.")
    if st.button("Accéder", key="go_dashboard"):
        switch_page("Dashboard")

with col3:
    st.markdown("### 📋 Explore les causalités en détail")
    st.markdown("Tableau filtrable des relations.")
    if st.button("Accéder", key="go_table"):
        switch_page("Table")
