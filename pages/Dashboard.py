import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Chargement des données ---
fact_data = pd.read_csv("data/fact_data.csv", sep=";")
fact_data["Measure Date"] = pd.to_datetime(fact_data["Measure Date"], dayfirst=True)
fact_data["Year"] = fact_data["Measure Date"].dt.year

# --- Filtres (dans la sidebar) ---
with st.sidebar:
    st.header("Filtres")

    kpi_options = fact_data["kpi_name"].unique()
    selected_kpi = st.selectbox("Sélectionner un KPI", options=kpi_options)

    years = sorted(fact_data["Year"].unique())
    selected_years = st.multiselect("Années", options=years, default=years)

    min_date = fact_data["Measure Date"].min()
    max_date = fact_data["Measure Date"].max()
    date_range = st.date_input("Période", value=[min_date, max_date])

# --- Filtrage des données ---
filtered_data = fact_data[
    (fact_data["kpi_name"] == selected_kpi) &
    (fact_data["Year"].isin(selected_years)) &
    (fact_data["Measure Date"] >= pd.to_datetime(date_range[0])) &
    (fact_data["Measure Date"] <= pd.to_datetime(date_range[1]))
]

# --- En-tête page ---
st.title("Dashboard de KPIs")
st.markdown(f"### KPI sélectionné : {selected_kpi}")

# --- Indicateurs clés ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Valeur moyenne", f"{filtered_data_
