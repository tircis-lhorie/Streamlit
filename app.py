# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# --- Interface Streamlit ---
st.set_page_config(page_title="TIRCIS Dashboard", layout="wide")
st.title("\U0001F9E0 Visualisation des causalités entre KPIs")
st.markdown("This app visualizes causal analysis between KPIs of Northwind data.")


page = st.sidebar.selectbox("Navigation", ["Accueil", "Graphe de Causalité", "Dashboard de KPIs"])

if page == "Accueil":
    st.title("Bienvenue")
elif page == "Graphe":
    st.title("Graphe de causalité")





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
dim_kpis = pd.read_csv("dim_kpis.csv", sep=";")
fact_links = pd.read_csv("fact_links.csv", sep=";")

fact_links = fact_links[fact_links["weight"] > 0]





# Sidebar
st.sidebar.image("Logo Linkedin.png", width=150)
st.sidebar.subheader("About This App")
st.sidebar.info(
    """
    Cette application permet de visualiser les liens de causalité entre les indicateurs de performance (KPIs) 
    d'une organisation. 

    Le graphe représente les KPIs comme des nœuds, reliés entre eux par des flèches indiquant des relations causales 
    identifiées statistiquement.

    Utilisez les filtres pour explorer les indicateurs par catégorie BSC, durabilité, ou poids du lien.
    """
)

# Filtres Sidebar
with st.sidebar:
    st.header("Filtres avancés")
    bsc_filter = st.multiselect("Filtrer par catégorie BSC", dim_kpis['bsc_category'].dropna().unique())
    sust_filter = st.selectbox("Durable uniquement ?", ["Tous", "Oui uniquement", "Non uniquement"])




col1, col2, col3, col4 = st.columns(4)
bsc_view = col1.toggle("Vue BSC", value=False)
signs_on = col2.toggle("Afficher les signes", value=False)
sust_on = col3.toggle("Colorer durabilité", value=True)
weights_on = col4.toggle("Épaisseur selon poids", value=False)


# Merge noms KPIs
fact_links = fact_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='From_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'kpi_from_name'})
fact_links = fact_links.merge(dim_kpis[['kpi_id', 'kpi_name']], left_on='To_id', right_on='kpi_id', how='left').rename(columns={'kpi_name': 'kpi_to_name'})

# Appliquer les filtres
if bsc_filter:
    fact_links = fact_links[fact_links['bsc_from_cat'].isin(bsc_filter) | fact_links['bsc_to_cat'].isin(bsc_filter)]

if sust_filter == "Oui uniquement":
    fact_links = fact_links[(fact_links['kpi_from_is_sust'] == 'Yes') | (fact_links['kpi_to_is_sust'] == 'Yes')]
elif sust_filter == "Non uniquement":
    fact_links = fact_links[(fact_links['kpi_from_is_sust'] == 'No') & (fact_links['kpi_to_is_sust'] == 'No')]



# Données pour le graphe
kpi_from_list = fact_links['kpi_from_name'].tolist()
kpi_to_list = fact_links['kpi_to_name'].tolist()
all_kpis = list(set(kpi_from_list + kpi_to_list))

# Positionnement
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

# Couleurs
node_colors = {kpi: "gray" for kpi in all_kpis}
if sust_on:
    for _, row in fact_links.iterrows():
        if row['kpi_from_is_sust'] == 'Yes':
            node_colors[row['kpi_from_name']] = '#3BAA5D'
        if row['kpi_to_is_sust'] == 'Yes':
            node_colors[row['kpi_to_name']] = '#3BAA5D'

# Arêtes
edges = [(row['kpi_from_name'], row['kpi_to_name'], row['weight'], row['sign']) for _, row in fact_links.iterrows()]
edge_widths = [2 + (w * 4 / 10) if weights_on else 2 for _, _, w, _ in edges]
edge_labels = {(s, e): '+' if sign == 'Positive' else '-' for s, e, _, sign in edges}

# Affichage graphique
fig, ax = plt.subplots(figsize=(18, 11))
node_radius = 0.13
for node, (x, y) in nodes_position.items():
    ax.scatter(x, y, s=6000, color=node_colors[node], zorder=3)
    ax.text(x, y, format_label(node), ha='center', va='center', fontsize=12, fontweight='bold', color='white', zorder=4)

for (start, end, weight, sign), width in zip(edges, edge_widths):
    posA, posB = adjust_arrow_positions(nodes_position[start], nodes_position[end], node_radius)
    arrow = FancyArrowPatch(posA, posB, arrowstyle='-|>', mutation_scale=20, color='black', linewidth=width, connectionstyle="arc3,rad=0.1", zorder=2)
    ax.add_patch(arrow)

if signs_on:
    for (start, end), label in edge_labels.items():
        mid_x = (nodes_position[start][0] + nodes_position[end][0]) / 2
        mid_y = (nodes_position[start][1] + nodes_position[end][1]) / 2
        ax.text(mid_x, mid_y, label, fontsize=16, bbox=dict(facecolor='white', edgecolor='none'), ha='center', va='center')

ax.set_xlim(-1.5, 4 if bsc_view else 1.5)
ax.set_ylim(0, 12 if bsc_view else 1.5)
ax.axis('off')
st.pyplot(fig)

# Export
st.download_button("🔍 Télécharger le graphe PNG", data=fig_to_bytes(fig), file_name="kpi_graph.png")

# Table
st.subheader("📊 Tableau des liens causaux")
st.dataframe(fact_links[['kpi_from_name', 'kpi_to_name', 'weight', 'sign', 'granger p-val', 'urgency']])

# Fonction pour convertir figure matplotlib en bytes
import io
def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    return buf.getvalue()

