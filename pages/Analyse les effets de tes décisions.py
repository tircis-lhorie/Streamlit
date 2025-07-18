import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import io

# --- Mise à l'échelle globale ---
scale = 1  # Modifie cette variable pour ajuster toutes les tailles

# Si l'utilisateur n'est pas authentifié
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Vous devez être connecté pour accéder à cette page.")
    if st.button("Retour à la page de connexion"):
        st.switch_page("app.py") 
    st.stop()

st.set_page_config(page_title="TIRCIS Dashboard",
                   page_icon="image/icon-transparent.png",
                   layout="wide")
st.logo("image/GIF2.gif", icon_image="image/icon.png")
st.title("Visualisation des causalités entre KPIs")
st.markdown("""
Cette application permet de visualiser les **liens de causalité** entre les indicateurs de performance (KPIs) 
d'une organisation.  
Le graphe représente les KPIs comme des nœuds, reliés entre eux par des flèches indiquant des relations causales 
identifiées statistiquement.

Utilisez les filtres pour explorer les indicateurs par **catégorie BSC**, **durabilité** ou **poids du lien**.
""")




# --- Fonctions utilitaires ---
def format_label(label):
    return label.replace(' ', '\n')

def adjust_arrow_positions(start_pos, end_pos, node_radius):
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    dx, dy = end_x - start_x, end_y - start_y
    distance = np.hypot(dx, dy)
    if distance == 0:
        return start_pos, end_pos
    dx /= distance
    dy /= distance
    return (start_x + dx * node_radius, start_y + dy * node_radius), (end_x - dx * node_radius, end_y - dy * node_radius)




# --- Chargement des données ---
dim_kpis = pd.read_csv("data/dim_kpis.csv", sep=";")
fact_links = pd.read_csv("data/fact_links.csv", sep=";")
fact_links = fact_links[fact_links["weight"] > 0]




# Filtres Sidebar
with st.sidebar:
    st.header("Filtres avancés")
    bsc_filter = st.multiselect("Filtrer par catégorie BSC", dim_kpis['bsc_category'].dropna().unique())
    sust_filter = st.selectbox("Durable uniquement ?", ["Tous", "Oui uniquement", "Non uniquement"])
st.sidebar.markdown("---")
st.sidebar.subheader("À propos de TIRCIS")
st.sidebar.markdown("<p style='color: white;'> <b>TIRCIS</b> est une spin-off de l'Université de Namur spécialisée en <b>Business Intelligence</b>. <br><br>Notre solution permet de <b>cartographier les liens de causalité entre les KPIs</b> d’une organisation afin d’anticiper les effets de chaque décision. <br><br>Contact: <u>tircis@unamur.be</u></p>", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stButton"] button {
    color: #CCCCCC !important;
    border: 2px solid #CCCCCC !important;
    background-color: white !important;
    border-radius: 12px;
    font-weight: normal;
    transition: all 0.2s ease-in-out;
}

div[data-testid="stButton"] button:hover {
    color: #FFA500 !important;
    border: 2px solid #FFA500 !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

def filter_button(label, key):
    active = st.session_state.get(key, False)
    clicked = st.button(label, key=key + "_btn")
    if clicked:
        st.session_state[key] = not active

    # Style dynamique basé sur l'état
    active_color = "#FFA500"
    inactive_color = "#CCCCCC"
    background = "#FFF5E6" if st.session_state[key] else "white"
    text_color = active_color if st.session_state[key] else inactive_color
    border_color = active_color if st.session_state[key] else inactive_color
    font_weight = "bold" if st.session_state[key] else "normal"

    st.markdown(f"""
        <style>
        div[data-testid="stButton"][data-key="{key}_btn"] button {{
            color: {text_color} !important;
            border: 2px solid {border_color} !important;
            background-color: {background} !important;
            font-weight: {font_weight} !important;
            border-radius: 12px;
        }}
        </style>
    """, unsafe_allow_html=True)


# Initialiser filtres
for key, default in {
    "bsc_view": False,
    "signs_on": False,
    "sust_on": False,
    "weights_on": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default



col1, col2, col3, col4, spacer = st.columns([1,1,1,1,2])
with col1:
    filter_button("Passer en vue BSC", "bsc_view")
with col2:
    filter_button("Afficher les signes", "signs_on")
with col3:
    filter_button("Colorer durabilité", "sust_on")
with col4:
    filter_button("Épaisseur selon poids", "weights_on")


bsc_view = st.session_state["bsc_view"]
signs_on = st.session_state["signs_on"]
sust_on = st.session_state["sust_on"]
weights_on = st.session_state["weights_on"]

fact_links = fact_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='From_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'kpi_from_name'})
fact_links = fact_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='To_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'kpi_to_name'})

if bsc_filter:
    fact_links = fact_links[fact_links['bsc_from_cat'].isin(bsc_filter) | fact_links['bsc_to_cat'].isin(bsc_filter)]
if sust_filter == "Oui uniquement":
    fact_links = fact_links[(fact_links['kpi_from_is_sust'] == 'Yes') | (fact_links['kpi_to_is_sust'] == 'Yes')]
elif sust_filter == "Non uniquement":
    fact_links = fact_links[(fact_links['kpi_from_is_sust'] == 'No') & (fact_links['kpi_to_is_sust'] == 'No')]

kpi_from_list = fact_links['kpi_from_name'].tolist()
kpi_to_list = fact_links['kpi_to_name'].tolist()
all_kpis = list(set(kpi_from_list + kpi_to_list))

nodes_position = {}
if bsc_view:
    x_pos = {"Finance": 0.6, "Customer": 0.8, "Internal Business Processes": 0.7, "Learning and Growth": 0.9}
    y_val = {"Finance": 10, "Customer": 8, "Internal Business Processes": 6, "Learning and Growth": 4}
    kpi_x, na_y = {}, 9
    for _, row in fact_links.iterrows():
        for role in ['from', 'to']:
            kpi = row[f'kpi_{role}_name']
            cat = row[f'bsc_{role}_cat']
            if cat != 'n.a':
                if kpi not in kpi_x:
                    kpi_x[kpi] = x_pos.get(cat, 1)
                    x_pos[cat] += 0.5
                nodes_position[kpi] = (kpi_x[kpi], y_val.get(cat, 2))
            else:
                if kpi not in nodes_position:
                    nodes_position[kpi] = (1.5, na_y)
                    na_y -= 2
else:
    angles = np.linspace(0, 2 * np.pi, len(all_kpis), endpoint=False)
    nodes_position = {kpi: (np.cos(a), np.sin(a)) for kpi, a in zip(all_kpis, angles)}

node_colors = {kpi: "gray" for kpi in all_kpis}
if sust_on:
    for _, row in fact_links.iterrows():
        if row['kpi_from_is_sust'] == 'Yes':
            node_colors[row['kpi_from_name']] = '#3BAA5D'
        if row['kpi_to_is_sust'] == 'Yes':
            node_colors[row['kpi_to_name']] = '#3BAA5D'

edges = [(row['kpi_from_name'], row['kpi_to_name'], row['weight'], row['sign']) for _, row in fact_links.iterrows()]
edge_widths = [scale * (2 + (w * 4 / 10)) if weights_on else 2 * scale for _, _, w, _ in edges]
edge_labels = {(s, e): '+' if sign == 'Positive' else '-' for s, e, _, sign in edges}

fig, ax = plt.subplots(figsize=(8 * scale, 5 * scale))
fig.patch.set_facecolor('none')
ax.set_facecolor('none')
node_radius = 0.05 * scale
for node, (x, y) in nodes_position.items():
    ax.scatter(x, y, s=2000 * scale, color=node_colors[node], zorder=3)
    ax.text(x, y, format_label(node), ha='center', va='center', fontsize=6 * scale, fontweight='bold', color='white', zorder=4)

for (start, end, weight, sign), width in zip(edges, edge_widths):
    posA, posB = adjust_arrow_positions(nodes_position[start], nodes_position[end], node_radius)
    arrow = FancyArrowPatch(posA, posB, arrowstyle='-|>', mutation_scale=10 * scale, color='black', linewidth=width, connectionstyle="arc3,rad=0.1", zorder=2)
    ax.add_patch(arrow)

if signs_on:
    for (start, end), label in edge_labels.items():
        mid_x = (nodes_position[start][0] + nodes_position[end][0]) / 2
        mid_y = (nodes_position[start][1] + nodes_position[end][1]) / 2
        ax.text(mid_x, mid_y, label, fontsize=16 * scale, bbox=dict(facecolor='white', edgecolor='none'), ha='center', va='center')

if bsc_view:
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 13)
else:
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.7, 1.7)

ax.axis('off')
plt.tight_layout()
st.pyplot(fig)
