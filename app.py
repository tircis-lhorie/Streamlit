# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# --- Liste des PIN autorisés ---
AUTHORIZED_PINS = {"1234", "5678"}

# --- Initialiser session ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Si non authentifié, afficher la page de login ---
if not st.session_state.authenticated:
    st.title("🔐 Entrez votre code PIN")

    col1, col2, col3, col4 = st.columns(4)
    pin_digits = []
    for i, col in enumerate([col1, col2, col3, col4]):
        with col:
            digit = st.text_input(
                label="",
                max_chars=1,
                key=f"digit_{i}",
                type="password",
                label_visibility="collapsed"
            )
            pin_digits.append(digit)

    # JavaScript : focus auto (injecté après les champs)
    st.components.v1.html("""
        <script>
        const inputs = window.parent.document.querySelectorAll('input[type="password"]');
        inputs.forEach((input, index) => {
            input.addEventListener('input', () => {
                if (input.value.length === 1 && index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            });
        });
        </script>
    """, height=0)

    # --- Validation du PIN ---
    pin_entered = "".join(pin_digits)

    if st.button("Valider"):
        if pin_entered in AUTHORIZED_PINS:
            st.success("Accès autorisé ✅")
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Code PIN incorrect ❌")
    st.stop()

# --- Si authentifié, continuer ---
st.success("Bienvenue ! Vous êtes connecté 🔓")


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.sidebar.image("image/logo.png", use_container_width=True)

st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")
