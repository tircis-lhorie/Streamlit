import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.logo("image/GIF2.gif", icon_image="image/icon.png")

# --- Chargement des données ---
fact_data = pd.read_csv("data/fact_data.csv", sep=";")
fact_data["Measure Date"] = pd.to_datetime(fact_data["Measure Date"], dayfirst=True)
fact_data["Year"] = fact_data["Measure Date"].dt.year

# --- Filtres (dans la sidebar) ---
with st.sidebar:
    st.header("Filtres")

    # Filtre par KPI (un seul)
    kpi_options = fact_data["kpi_name"].unique()
    selected_kpi = st.selectbox("Sélectionner un KPI", options=kpi_options)

    # Filtre par années
    years = sorted(fact_data["Year"].unique())
    selected_years = st.multiselect("Années", options=years, default=years)

    # Filtre par période
    min_date = fact_data["Measure Date"].min()
    max_date = fact_data["Measure Date"].max()
    date_range = st.date_input("Période", value=[min_date, max_date])

st.sidebar.subheader("À propos de TIRCIS")
st.sidebar.info(
    """
    **TIRCIS** est une spin-off de l'Université de Namur spécialisée en **Business Intelligence** augmentée.
    
    Notre solution permet de **cartographier les liens de causalité entre les KPIs** d’une organisation afin d’anticiper les effets de chaque décision.

    Contact: tircis@unamur.be    """
)

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
    st.metric("Valeur moyenne", f"{filtered_data['Measure'].mean():.2f}")
with col2:
    st.metric("Valeur max", f"{filtered_data['Measure'].max():.2f}")

# --- Graphique d'évolution ---
st.subheader("Évolution temporelle")
fig, ax = plt.subplots()
fig.patch.set_facecolor("#F0F0F0")     # ou .set_alpha(0.0) pour transparent
ax.set_facecolor("#F0F0F0")           # ou "none" pour transparent

ax.plot(filtered_data["Measure Date"], filtered_data["Measure"], marker='o')
ax.set_xlabel("Date")
ax.set_ylabel("Mesure")
ax.set_title(f"Évolution du KPI : {selected_kpi}")

st.pyplot(fig)

# --- Tableau des données ---
st.subheader("Données détaillées")
st.dataframe(filtered_data.sort_values("Measure Date", ascending=False))
