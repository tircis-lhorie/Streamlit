# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")


# --- Liste des PIN autorisés ---
AUTHORIZED_PINS = {"2024", "1234"} 

# --- CSS pour centrer et styliser ---
st.markdown("""
<style>
.centered {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}
input[type="password"] {
    font-size: 24px !important;
    letter-spacing: 10px;
    text-align: center;
    width: 150px !important;
}
.stButton button {
    background-color: #FFA500;
    color: white;
    border: none;
    padding: 0.75em 2em;
    font-size: 16px;
    border-radius: 25px;
    cursor: pointer;
    transition: background-color 0.2s;
}
.stButton button:hover {
    background-color: #e69500;
}
</style>
""", unsafe_allow_html=True)

# --- Interface centrée ---
st.markdown('<div class="centered">🔐</div>', unsafe_allow_html=True)
st.markdown('<div class="centered"><h4>Entrez votre code PIN</h4><p>Veuillez entrer le code à 4 chiffres</p></div>', unsafe_allow_html=True)

pin = st.text_input("PIN", type="password", label_visibility="collapsed")

st.markdown('<div class="centered">', unsafe_allow_html=True)
if st.button("Se connecter"):
    if pin in AUTHORIZED_PINS:
        st.success("Connexion réussie ✅")
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.error("Code PIN incorrect ❌")
st.markdown('</div>', unsafe_allow_html=True)


# --- Interface Streamlit ---
st.sidebar.image("image/logo.png", use_container_width=True)

st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")
