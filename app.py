# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# --- Configuration utilisateur simple ---
USERS = {
    "corentin.burnay@unamur.be": "1234",  
    "lhorie.pirnay@unamur.be": "1234"
}

# --- Session pour savoir si l'utilisateur est authentifié ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("🔐 Connexion requise")
    username = st.text_input("Adresse email")
    password = st.text_input("Code PIN", type="password")
    if st.button("Se connecter"):
        if username in USERS and USERS[username] == password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Identifiants incorrects.")

if not st.session_state.authenticated:
    login()
    st.stop()


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.sidebar.image("image/logo.png", use_container_width=True)

st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")

#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

