# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")

# Afficher le logo dans le coin supérieur gauche
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("image/logo.png", use_container_width=True)


page = st.sidebar.selectbox("Navigation", ["Accueil", "Graphe de Causalité", "Dashboard de KPIs"])

