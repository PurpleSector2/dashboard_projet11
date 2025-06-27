import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des fichiers
@st.cache_data
def load_data():
    df_100 = pd.read_csv("df_100.csv")
    df_kmeans0 = pd.read_csv("df_kmeans0.csv")
    df_ranking = pd.read_csv("df_ranking.csv")
    df_ranking_K0 = pd.read_csv("df_ranking_K0.csv")
    return df_100, df_kmeans0, df_ranking, df_ranking_K0

df_100, df_kmeans0, df_ranking, df_ranking_K0 = load_data()

# Sélecteur de dataset
choix = st.sidebar.radio("Choisir l'étude à afficher :", ["Etude sur l'échantillon entier", "Etude sur un cluster spécifique"])

if choix == "Etude sur l'échantillon entier":
    st.title("📊 Analyse : Échantillon entier")
    df = df_100.copy()
    df_rk = df_ranking.copy()
else:
    st.title("📊 Analyse : Cluster spécifique (Kmeans 0)")
    df = df_kmeans0.copy()
    df_rk = df_ranking_K0.copy()

# Graphique 1 : Top 5 Part_terre_bio
st.subheader("🌱 Top 5 pays avec le plus de terres bio")
df_top5_bio = df[df['Pays'] != 'Médiane'].sort_values('Part_terre_bio', ascending=False).head(5)
st.dataframe(df_top5_bio[['Pays', 'Part_terre_bio']])

# Graphique 2 : Nb_dépassement_median
st.subheader("🔥 Top 20 dépassements de médiane")
top_20 = df[df['Pays'] != 'Médiane'].sort_values("Nb_dépassement_median", ascending=False).head(20)
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_20, x="Nb_dépassement_median", y="Pays", palette="Reds_r", ax=ax1)
ax1.set_title("🔥 Top 20 pays – Dépassement de médiane")
ax1.set_xlabel("Nb de variables où le pays dépasse la médiane")
ax1.set_ylabel("Pays")
ax1.grid(axis="x", linestyle="--", alpha=0.6)
st.pyplot(fig1)

# Graphique 3 : Ratio volaille import
st.subheader("📊 Ratio Volaille Import / Volaille Dispo Intérieure")
df['Ratio_Volaille_Import'] = df['Volaille_Import'] / df['Volaille_Dispo_int']
df_plot_ratio = df[(df['Pays'] != 'Médiane') & df['Ratio_Volaille_Import'].notnull() & (df['Ratio_Volaille_Import'] != float('inf'))]
df_plot_ratio = df_plot_ratio.sort_values('Ratio_Volaille_Import', ascending=False).head(20)
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x='Ratio_Volaille_Import', y='Pays', data=df_plot_ratio, palette='Reds_r', ax=ax2)
ax2.set_title("📊 Ratio Volaille Import / Volaille Disponibilité Intérieure", fontsize=16)
ax2.set_xlabel("Ratio (Volaille_Import / Volaille_Dispo_int)")
ax2.set_ylabel("Pays")
ax2.set_xlim(0, 3)
ax2.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig2)

# Graphique 4 : Classement des pays proches du profil France
st.subheader("🌍 Classement des pays proches du profil France")

df_plot_distance = df[
    (df['Pays'] != 'FRANCE') & (df['Pays'] != 'Médiane') & df['Distance_France'].notnull()
].sort_values('Distance_France').head(5)

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='Distance_France', y='Pays', data=df_plot_distance, palette='Blues_r', ax=ax3)

ax3.set_title("📊 Classement des pays les + proches du profil France\n(basé sur les variables business)", fontsize=14)
ax3.set_xlabel("Indice de similarité (distance normalisée par variable)", fontsize=12)
ax3.set_ylabel("Pays", fontsize=12)
fig3.text(0.5, -0.1, 
    "👉 Ce classement indique les pays les plus proches de la France sur le plan business.\n"
    "⚠️ Distance faible = profil proche.\n"
    "NB : la distance est un indicateur relatif, non une unité absolue.",
    ha="center", fontsize=10)
ax3.grid(axis='x', linestyle='--', alpha=0.6)
st.pyplot(fig3)

# Graphique 5 : Podium
st.subheader("🏆 Podium des pays les plus compétitifs")
df_podium = df_rk.head(3).sort_values('Total_Score')
df_podium['Rang'] = [1, 2, 3]
colors = ['#FFD700', '#C0C0C0', '#CD7F32']
fig4, ax4 = plt.subplots(figsize=(8, 6))
bars = ax4.bar(df_podium['Rang'], [1, 0.9, 0.8], color=colors, tick_label=df_podium['Pays'])
for bar, score in zip(bars, df_podium['Total_Score']):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f"Score: {int(score)}", ha='center', fontsize=12, fontweight='bold')
ax4.set_title("🏆 Podium des pays les + compétitifs", fontsize=16)
ax4.set_ylim(0, 1.2)
ax4.set_yticks([])
fig4.text(0.5, -0.08, "👉 Le podium est basé sur le Total_Score = somme des rangs sur les variables business.", ha="center", fontsize=10)
st.pyplot(fig4)

# Section conclusion
st.markdown("___")
st.subheader("📝 Conclusion")
st.markdown("""
**Au vu des analyses menées sur les deux études, nous pouvons conclure de la façon suivante :**

- 🇮🇹 **Implantation** : L’Italie semble être le choix optimal pour une implantation physique. Le marché est vaste, mature, la consommation de volaille est élevée, et le pays est une terre d’accueil favorable au développement du bio.

- 🇦🇪 **Exportation** : Les Émirats Arabes Unis représentent une excellente opportunité d’exportation : pays riche, forte consommation de volaille, dépendance aux importations. Cependant, une adaptation au marché Halal est indispensable.

- 🇳🇱 **Alternative UE** : Si l’adaptation au marché Halal représente une contrainte, une **alternative stratégique** plus proche pourrait être les **Pays-Bas**, qui offrent des conditions similaires (forte consommation, dépendance à l’import), tout en étant situés en Union Européenne et à proximité immédiate de la France.
""")