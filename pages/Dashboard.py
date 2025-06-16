import streamlit as st
import pandas as pd
import altair as alt

# --- Chargement des données ---
df = pd.read_csv("data/fact_data.csv", sep=";")

# --- Nettoyage / parsing ---
df['Measure Date'] = pd.to_datetime(df['Measure Date'], errors='coerce')
df = df.dropna(subset=['Measure Date'])  # sécurité si erreur de parsing

# --- Titre ---
st.title("Dashboard de KPIs")
st.markdown("Visualisez les mesures temporelles de vos indicateurs de performance.")

# --- Filtres ---
with st.sidebar:
    st.header("Filtres")
    selected_kpis = st.multiselect("KPIs à afficher", df['kpi_name'].unique(), default=df['kpi_name'].unique()[:5])
    date_range = st.date_input("Période", [df['Measure Date'].min(), df['Measure Date'].max()])

# --- Application des filtres ---
start_date, end_date = date_range
filtered_df = df[
    (df['kpi_name'].isin(selected_kpis)) &
    (df['Measure Date'] >= pd.to_datetime(start_date)) &
    (df['Measure Date'] <= pd.to_datetime(end_date))
]

# --- Graphique évolutif ---
st.subheader("Évolution temporelle")
chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x='Measure Date:T',
    y='Measure:Q',
    color='kpi_name:N',
    tooltip=['kpi_name', 'Measure', 'Measure Date']
).properties(height=400, width=700)

st.altair_chart(chart, use_container_width=True)

# --- Tableau ---
st.subheader("Tableau des données")
st.dataframe(filtered_df.sort_values(by="Measure Date"), use_container_width=True)

# --- Export CSV ---
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Télécharger les données filtrées", data=csv, file_name="report_kpis.csv", mime="text/csv")
