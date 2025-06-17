# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from streamlit_extras.switch_page_button import switch_page


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.logo("image/GIF2.gif", icon_image="image/icon.png")

st.sidebar.subheader("À propos de TIRCIS")
st.sidebar.markdown(
    """
    **TIRCIS** est une spin-off de l'Université de Namur spécialisée en **Business Intelligence** augmentée.
    
    Notre solution permet de **cartographier les liens de causalité entre les KPIs** d’une organisation afin d’anticiper les effets de chaque décision.

    Contact: tircis@unamur.be    """
)


st.sidebar.markdown("<p style='color: white;'> <b>TIRCIS</b> est une spin-off de l'Université de Namur spécialisée en <b>Business Intelligence</b> augmentée. <br>Notre solution permet de <b>cartographier les liens de causalité entre les KPIs</b> d’une organisation afin d’anticiper les effets de chaque décision. <br>Contact: tircis@unamur.be</p>", unsafe_allow_html=True)



# --- Liste des PIN autorisés ---
AUTHORIZED_PINS = {"1234", "5678"}  # à adapter

# --- Session pour savoir si l'utilisateur est authentifié ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.markdown(
        """
        <style>
        .centered-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .centered-container input {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True
    )

    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col1: st.image("image/moving_icon.gif",use_container_width=True)
            
        with col2:
            st.markdown('<div class="centered-container">', unsafe_allow_html=True)
            st.title("Connexion requise")
            st.subheader("Veuillez entrer votre code PIN pour accéder à l'application")
            pin = st.text_input("Code PIN à 4 chiffres", type="password", max_chars=4)
            if st.button("Se connecter"):
                if pin in AUTHORIZED_PINS:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Code PIN incorrect.")
            st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    login()
    st.stop()




st.title("Bienvenue")
st.markdown("Bienvenue sur votre espace TIRCIS.")

# Espacement
st.markdown("## ")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔄 Analyse les effets de tes décisions")
    st.markdown("Carte interactive pour comprendre les impacts.")
    if st.button("C’est parti !", key="page1"):
        switch_page("Analyse les effets de tes décisions")

with col2:
    st.markdown("### 📊 Découvre ton tableau de bord")
    st.markdown("Visualise tes données dans le temps.")
    if st.button("C’est parti !", key="page2"):
        switch_page("Découvre ton tableau de bord")

with col3:
    st.markdown("### 🔎 Explore les causalités en détail")
    st.markdown("Filtre et exporte les résultats complets.")
    if st.button("C’est parti !", key="page3"):
        switch_page("Explore les causalités en détail")
