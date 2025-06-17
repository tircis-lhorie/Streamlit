import streamlit as st
import pandas as pd

# --- Chargement des données ---
dim_kpis = pd.read_csv("data/dim_kpis.csv", sep=";")
fact_links = pd.read_csv("data/fact_links.csv", sep=";")
fact_links = fact_links[fact_links["weight"] > 0]

# --- Titre de la page ---
st.title("Tableau récapitulatif des causalité")
st.markdown("Vous trouverez ci-dessous l'intégralité des résultats des analyses de causalités entre les KPIs de votre entreprise.")

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



# --- Préparation du tableau filtré ---
filtered_df = fact_links[[
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
})

# --- Chargement des données complètes (non filtrées) ---
all_links = pd.read_csv("data/fact_links.csv", sep=";")
all_links = all_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='From_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'KPI Source'})
all_links = all_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='To_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'KPI Cible'})
all_links_export = all_links[[
    'KPI Source', 'KPI Cible', 'sign', 'weight',
    'granger p-val', 'granger F-stat', 'type_of_comfirming_analysis',
    'urgency', 'duration', 'granularity'
]].rename(columns={
    'sign': 'Signe',
    'weight': 'Poids',
    'granger p-val': 'p-valeur',
    'granger F-stat': 'F-stat',
    'type_of_comfirming_analysis': 'Méthode',
    'urgency': 'Urgence',
    'duration': 'Durée',
    'granularity': 'Granularité'
})

# --- Conversion en CSV ---
filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
all_csv = all_links_export.to_csv(index=False).encode("utf-8")

# --- Affichage côte à côte ---
col1, col2, spacer = st.columns(1, 1, 3)
with col1:
    st.download_button(
        label="↓ Télécharger toutes les données au format csv",
        data=filtered_csv,
        file_name="liens_kpis_complets.csv",
        mime="text/csv"
    )
with col2:
    st.download_button(
        label="↓ Télécharger les données filtrées au format csv",
        data=all_csv,
        file_name="liens_kpis_filtrés.csv",
        mime="text/csv"
    )




# --- KPIs synthétiques ---

# Top 3 causes les plus fréquentes
top_causes = fact_links['kpi_from_name'].value_counts().head(3)

# Top 3 effets les plus fréquemment impactés
top_effects = fact_links['kpi_to_name'].value_counts().head(3)

# Top 3 relations les plus fortes (en poids)
top_weights = fact_links.sort_values(by='weight', ascending=False).head(3)[
    ['kpi_from_name', 'kpi_to_name', 'weight']
]


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


