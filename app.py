# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# --- CSS pour le style des cases ---
st.markdown("""
    <style>
    .pin-input input {
        font-size: 32px;
        text-align: center;
        border: 2px solid #ccc;
        border-radius: 8px;
        width: 60px;
        height: 60px;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Création de 4 cases côte à côte ---
st.title("🔐 Entrer le code PIN")

cols = st.columns(4)
pin_digits = []

for i, col in enumerate(cols):
    with col:
        digit = st.text_input(f"", max_chars=1, key=f"digit_{i}", type="password", label_visibility="collapsed")
        pin_digits.append(digit)

# --- Validation du PIN ---
entered_pin = "".join(pin_digits)
AUTHORIZED_PINS = {"1234", "5678"}

if st.button("Valider"):
    if entered_pin in AUTHORIZED_PINS:
        st.success("PIN correct ✅")
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.error("PIN incorrect ❌")

# --- Blocage si pas encore connecté ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.stop()


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.sidebar.image("image/logo.png", use_container_width=True)

st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")
