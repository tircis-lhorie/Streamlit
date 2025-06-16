import streamlit as st
import pandas as pd
import altair as alt

# Chargement des données
fact_data = pd.read_csv("data/fact_data.csv", sep=";")
fact_data["Measure Date"] = pd.to_datetime(fact_data["Measure Date"])
fact_data["Measure Date"] = fact_data["Measure Date"].dt.strftime("%d/%m/%Y")

# Titre de la page
st.title("Dashboard de performance")

# Sélection du KPI (en haut de la page)
selected_kpi = st.selectbox("Sélectionnez un KPI", fact_data["kpi_name"].unique())

# Filtres dans la barre latérale
with st.sidebar:
    st.subheader("Filtres")
    date_range = st.date_input(
        "Période",
        value=[fact_data["Measure Date"].min(), fact_data["Measure Date"].max()]
    )
    agg_method = st.selectbox("Méthode d'agrégation", ["Moyenne", "Somme", "Max", "Min"])

# Filtrage
filtered = fact_data[
    (fact_data["kpi_name"] == selected_kpi) &
    (fact_data["Measure Date"] >= pd.to_datetime(date_range[0])) &
    (fact_data["Measure Date"] <= pd.to_datetime(date_range[1]))
]

# Agrégation
if agg_method == "Moyenne":
    agg_df = filtered.groupby("Measure Date")["Measure"].mean().reset_index()
elif agg_method == "Somme":
    agg_df = filtered.groupby("Measure Date")["Measure"].sum().reset_index()
elif agg_method == "Max":
    agg_df = filtered.groupby("Measure Date")["Measure"].max().reset_index()
else:
    agg_df = filtered.groupby("Measure Date")["Measure"].min().reset_index()

# Graphique
st.altair_chart(
    alt.Chart(agg_df)
    .mark_line(point=True)
    .encode(
        x="Measure Date:T",
        y="Measure:Q",
        tooltip=["Measure Date", "Measure"]
    )
    .properties(height=400, title=selected_kpi),
    use_container_width=True
)

# Tableau
st.subheader("Données sources")
st.dataframe(agg_df)
