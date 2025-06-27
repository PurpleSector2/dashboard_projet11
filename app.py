# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analyse ACP & Clustering", layout="wide")

# Chargement des fichiers CSV
@st.cache_data
def load_data():
    df_100 = pd.read_csv("df_100.csv")
    df_kmeans0 = pd.read_csv("df_kmeans0.csv")
    df_ranking = pd.read_csv("df_ranking.csv")
    df_ranking_K0 = pd.read_csv("df_ranking_K0.csv")
    return df_100, df_kmeans0, df_ranking, df_ranking_K0

df_100, df_kmeans0, df_ranking, df_ranking_K0 = load_data()

# Choix utilisateur
choix = st.sidebar.radio("📊 Sélectionner l'analyse :", ["Etude sur l'échantillon entier", "Etude sur le cluster cible (Kmeans 0)"])

# Définir les bons DataFrames
if choix == "Etude sur l'échantillon entier":
    df = df_100
    df_ranking_sel = df_ranking
else:
    df = df_kmeans0
    df_ranking_sel = df_ranking_K0

st.title("Analyse comparative des pays")
st.markdown(f"### {choix}")

# 🔥 Dépassement de médiane
st.subheader("🔥 Top 20 pays – Dépassement de médiane")
top_20 = df[df["Pays"] != "Médiane"].sort_values("Nb_dépassement_median", ascending=False).head(20)
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_20, x="Nb_dépassement_median", y="Pays", palette="Reds_r", ax=ax1)
ax1.set_title("🔥 Nb de variables dépassant la médiane")
ax1.set_xlabel("Nombre")
ax1.set_ylabel("Pays")
ax1.grid(axis="x", linestyle="--", alpha=0.6)
st.pyplot(fig1)

# 📊 Ratio volaille importée
st.subheader("📊 Ratio Volaille Import / Disponibilité intérieure")
df_plot_ratio = df[
    (df['Pays'] != 'Médiane') &
    df['Ratio_Volaille_Import'].notnull() &
    (df['Ratio_Volaille_Import'] != float('inf'))
].sort_values('Ratio_Volaille_Import', ascending=False).head(20)

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x='Ratio_Volaille_Import', y='Pays', data=df_plot_ratio, palette='Reds_r', ax=ax2)
ax2.set_xlim(0, 3)
ax2.set_title("📊 Dépendance à l'import de volaille")
ax2.set_xlabel("Ratio (Import / Dispo int)")
ax2.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig2)

# 📍 Pays proches du profil France (Distance)
st.subheader("📍 Pays les plus proches du profil France")
df_proches = df[(df['Pays'] != 'FRANCE') & (df['Pays'] != 'Médiane')].sort_values('Distance_France')
df_plot_distance = df_proches.head(5)

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='Distance_France', y='Pays', data=df_plot_distance, palette='Blues_r', ax=ax3)
ax3.set_title("📍 Distance par rapport au profil France")
ax3.set_xlabel("Distance normalisée")
ax3.grid(axis='x', linestyle='--', alpha=0.6)
st.pyplot(fig3)

# 🏆 Podium des pays les plus compétitifs
st.subheader("🏆 Podium des pays les + compétitifs")
df_podium = df_ranking_sel.head(3).copy().sort_values('Total_Score')
df_podium['Rang'] = [1, 2, 3]

colors = ['#FFD700', '#C0C0C0', '#CD7F32']
fig4, ax4 = plt.subplots(figsize=(8, 6))
bars = ax4.bar(df_podium['Rang'], [1, 0.9, 0.8], color=colors, tick_label=df_podium['Pays'])

for bar, score in zip(bars, df_podium['Total_Score']):
    ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
             f"Score: {int(score)}", ha='center', fontsize=12, fontweight='bold')

ax4.set_ylim(0, 1.2)
ax4.set_yticks([])
ax4.set_title("🏆 Classement basé sur le Total_Score")
st.pyplot(fig4)

# ✅ Optionnel : afficher les Top 5 sur Part_terre_bio
st.subheader("✅ Top 5 sur Part_terre_bio")
df_top5_bio = df[df['Pays'] != 'Médiane'].sort_values('Part_terre_bio', ascending=False).head(5)
st.dataframe(df_top5_bio[['Pays', 'Part_terre_bio']])