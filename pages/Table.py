import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

st.title("Tableau de causalité")
st.markdown("Explorez les effets de causalités entre les KPIs de votre entreprise !")
import streamlit as st
import pandas as pd

# --- Chargement des données ---
dim_kpis = pd.read_csv("data/dim_kpis.csv", sep=";")
fact_links = pd.read_csv("data/fact_links.csv", sep=";")
fact_links = fact_links[fact_links["weight"] > 0]

# --- Titre de la page ---
st.title("Tableau de causalité")
st.markdown("Explorez les effets de causalités entre les KPIs de votre entreprise !")

# --- Merge pour afficher les noms des KPIs ---
fact_links = fact_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='From_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'kpi_from_name'})
fact_links = fact_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='To_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'kpi_to_name'})

# --- Filtres utilisateur ---
with st.sidebar:
    st.subheader("Filtres")
    bsc_filter = st.multiselect("Catégorie BSC", dim_kpis['bsc_category'].dropna().unique())
    sign_filter = st.radio("Signe du lien", ["Tous", "Positive", "Negative"])
    min_weight = st.slider("Poids minimum", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# --- Application des filtres ---
if bsc_filter:
    fact_links = fact_links[
        fact_links['bsc_from_cat'].isin(bsc_filter) |
        fact_links['bsc_to_cat'].isin(bsc_filter)
    ]

if sign_filter != "Tous":
    fact_links = fact_links[fact_links['sign'] == sign_filter]

fact_links = fact_links[fact_links['weight'] >= min_weight]


# --- KPIs synthétiques ---

# Top 3 causes les plus fréquentes
top_causes = fact_links['kpi_from_name'].value_counts().head(3)

# Top 3 effets les plus fréquemment impactés
top_effects = fact_links['kpi_to_name'].value_counts().head(3)

# Top 3 relations les plus fortes (en poids)
top_weights = fact_links.sort_values(by='weight', ascending=False).head(3)[
    ['kpi_from_name', 'kpi_to_name', 'weight']
]

# Affichage en 3 colonnes
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔥 Top 3 causes")
    for kpi, count in top_causes.items():
        st.markdown(f"• **{kpi}** ({count} liens)")

with col2:
    st.subheader("🎯 Top 3 effets")
    for kpi, count in top_effects.items():
        st.markdown(f"• **{kpi}** ({count} liens)")

with col3:
    st.subheader("⚖️ Top 3 liens (poids)")
    for _, row in top_weights.iterrows():
        st.markdown(f"• **{row['kpi_from_name']} ➜ {row['kpi_to_name']}** ({row['weight']:.2f})")



# --- Affichage du tableau ---
st.dataframe(
    fact_links[[
        'kpi_from_name', 'kpi_to_name', 'sign', 'weight',
        'granger p-val', 'granger F-stat', 'type_of_comfirming_analysis',
        'urgency', 'duration', 'granularity'
    ]].rename(columns={
        'kpi_from_name': 'KPI Source',
        'kpi_to_name': 'KPI Cible',
        'sign': 'Signe',
        'weight': 'Poids',
        'granger p-val': 'p-valeur',
        'granger F-stat': 'F-stat',
        'type_of_comfirming_analysis': 'Méthode',
        'urgency': 'Urgence',
        'duration': 'Durée',
        'granularity': 'Granularité'
    }),
    use_container_width=True
)
