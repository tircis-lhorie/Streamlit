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

st.sidebar.image("image/logo.png", use_container_width=True)
