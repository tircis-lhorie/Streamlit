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

page = st.sidebar.selectbox("Navigation", ["Accueil", "Graphe de Causalité", "Dashboard de KPIs"])

# Sidebar
#st.sidebar.image("image/logo.png", width=150)
st.sidebar.subheader("About This App")
st.sidebar.info(
    """
    Cette application permet de visualiser les liens de causalité entre les indicateurs de performance (KPIs) 
    d'une organisation. 

    Le graphe représente les KPIs comme des nœuds, reliés entre eux par des flèches indiquant des relations causales 
    identifiées statistiquement.

    Utilisez les filtres pour explorer les indicateurs par catégorie BSC, durabilité, ou poids du lien.
    """
)




