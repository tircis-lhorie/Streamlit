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
st.sidebar.image("image/logo.png", width=150)





