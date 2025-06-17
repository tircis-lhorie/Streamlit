# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

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


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.sidebar.image("image/logo.png", use_container_width=True)

st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")
