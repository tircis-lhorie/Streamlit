import streamlit as st
import pandas as pd
from datetime import timedelta, datetime

# Set page config
st.set_page_config(page_title="Test TIRCIS Dashboard", layout="wide")

# Helper functions
@st.cache_data
def load_data():
    data = pd.read_csv("dim_kpis.csv")
    return kpi-data



