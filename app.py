# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from streamlit_extras.switch_page_button import switch_page


# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard",
                   page_icon="image/icon-transparent.png",
                   layout="wide")
st.logo("image/GIF2.gif", icon_image="image/icon.png")

st.sidebar.subheader("À propos de TIRCIS")
st.sidebar.markdown("<p style='color: white;'> <b>TIRCIS</b> est une spin-off de l'Université de Namur spécialisée en <b>Business Intelligence</b>. <br><br>Notre solution permet de <b>cartographier les liens de causalité entre les KPIs</b> d’une organisation afin d’anticiper les effets de chaque décision. <br><br>Contact: <u>tircis@unamur.be</u></p>", unsafe_allow_html=True)



# --- Liste des PIN autorisés ---
AUTHORIZED_USERS = {"lhorie.pirnay@unamur.be": "1234", "corentin.burnay@unamur.be": "1234"}

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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image("image/moving_icon.gif", use_container_width=True)

        with col2:
            st.markdown('<div class="centered-container">', unsafe_allow_html=True)
            st.title("Connexion requise")
            st.subheader("Veuillez entrer votre code PIN pour accéder à l'application")

            with st.form(key="login_form"):
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type="password")
                submitted = st.form_submit_button("Se connecter")
                if submitted:
                    if AUTHORIZED_USERS.get(username) == password:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects.")
            st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    login()
    st.stop()





st.title("Bienvenue")
st.markdown("Bienvenue sur l'application TIRCIS.")

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
