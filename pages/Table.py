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


def kpi_box(title, items, highlight=None):
    st.markdown(f"<h5 style='margin-bottom: 10px'>{title}</h5>", unsafe_allow_html=True)
    for i, item in enumerate(items):
        kpi_name = item[0]
        value = item[1]
        st.markdown(
            f"""
            <div style='
                background-color: #F0F2F6;
                border-left: 6px solid #6c6cff;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
            '>
                <strong>{kpi_name}</strong><br><span style='font-size: 12px;'>({value})</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# Préparer les 3 listes
top_causes_list = list(top_causes.items())
top_effects_list = list(top_effects.items())
top_weights_list = [(f"{row['kpi_from_name']} ➜ {row['kpi_to_name']}", f"{row['weight']:.2f}") for _, row in top_weights.iterrows()]

# Afficher dans 3 colonnes
col1, col2, col3 = st.columns(3)
with col1:
    kpi_box("Top 3 causes", top_causes_list)
with col2:
    kpi_box("Top 3 effets", top_effects_list)
with col3:
    kpi_box("Top 3 liens (poids)", top_weights_list)




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
