# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les DataFrames
df_filtré_clusters = pd.read_csv('df_filtré_clusters.csv')
df_ranking = pd.read_csv('df_ranking.csv')

# Variables numériques pour Analyse par variable
variables_numeriques = [
    col for col in df_filtré_clusters.columns
    if col not in ['Pays', 'Code ISO', 'Année', 'cluster', 'Volaille_vs_Median', 'Distance_France',
                   'Nb_dépassement_median', 'Ratio_Volaille_Import', 'globalRank']
    and pd.api.types.is_numeric_dtype(df_filtré_clusters[col])
]

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", [
    "Présentation",
    "Classement global",
    "Podium",
    "Analyse par variable",
    "Classement des pays proches France",
    "Ratio Volaille Import / Dispo intérieure"
])

# Présentation
if page == "Présentation":
    st.title("📊 Analyse comparative des pays - Dashboard")
    st.markdown("""
    👉 **Pays de référence : France**  
    👉 Objectifs :
    - Identifier les pays les + proches du profil France (Distance multi-variable)
    - Identifier les pays + dépendants de l'import en volaille (Ratio Volaille Import / Dispo intérieure)
    - Visualiser le classement global basé sur les rangs
    - Analyser chaque variable individuellement

    **Variables utilisées :**
    - `Distance_France`
    - `Ratio_Volaille_Import`
    - Variables business (pour Total_Score et Analyse par variable)
    """)

# Classement global
elif page == "Classement global":
    st.title("🏅 Classement global des pays")
    st.dataframe(df_ranking[['Pays', 'Total_Score']].sort_values('Total_Score'))

# Podium
elif page == "Podium":
    st.title("🏆 Podium des pays les plus compétitifs")

    df_podium = df_ranking.head(3).copy()
    df_podium = df_podium.sort_values('Total_Score', ascending=True)

    # Podium plot
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FFD700', '#C0C0C0', '#CD7F32']
    bars = ax.bar(df_podium['Pays'], [1, 0.9, 0.8], color=colors)

    for bar, score in zip(bars, df_podium['Total_Score']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"Score: {int(score)}", ha='center', fontsize=12, fontweight='bold')

    ax.set_ylim(0, 1.2)
    ax.set_title("Podium des pays", fontsize=16)
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_yticks([])

    st.pyplot(fig)

# Analyse par variable
elif page == "Analyse par variable":
    st.title("📈 Analyse par variable")
    variable = st.selectbox("Choisir une variable :", variables_numeriques)
    df_variable_rank = df_filtré_clusters[df_filtré_clusters['Pays'] != 'Médiane'][['Pays', variable]].sort_values(variable, ascending=False)

    # Barplot variable
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=variable,
        y='Pays',
        data=df_variable_rank.head(15),
        palette='Blues_r',
        ax=ax
    )

    ax.set_title(f"Classement sur {variable}", fontsize=14)
    ax.set_xlabel(variable)
    ax.set_ylabel("Pays")
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    st.pyplot(fig)

# Classement des pays proches France
elif page == "Classement des pays proches France":
    st.title("🏅 Classement des pays les + proches du profil France")
    
    df_proches_france = df_filtré_clusters[
        (df_filtré_clusters['Pays'] != 'FRANCE') &
        (df_filtré_clusters['Pays'] != 'Médiane') &
        (df_filtré_clusters['Distance_France'].notnull())
    ].sort_values('Distance_France', ascending=True)

    df_plot_distance = df_proches_france.head(5).copy()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='Distance_France',
        y='Pays',
        data=df_plot_distance,
        palette='Blues_r',
        ax=ax
    )

    ax.set_title("Classement des pays les + proches du profil France\n(basé sur la distance globale sur les variables business)", fontsize=14)
    ax.set_xlabel("Distance_France")
    ax.set_ylabel("Pays")
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    st.pyplot(fig)

# Ratio Volaille Import
elif page == "Ratio Volaille Import / Dispo intérieure":
    st.title("🍗 Ratio Volaille Import / Volaille Disponibilité Intérieure")

    df_plot_ratio = df_filtré_clusters[
        (df_filtré_clusters['Pays'] != 'Médiane') &
        (df_filtré_clusters['Ratio_Volaille_Import'].notnull()) &
        (df_filtré_clusters['Ratio_Volaille_Import'] != float('inf'))
    ].sort_values('Ratio_Volaille_Import', ascending=False)

    df_plot_ratio = df_plot_ratio.head(10).copy()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='Ratio_Volaille_Import',
        y='Pays',
        data=df_plot_ratio,
        palette='Reds_r',
        ax=ax
    )

    ax.set_title("Ratio Volaille Import / Volaille Disponibilité Intérieure", fontsize=16)
    ax.set_xlabel("Ratio (Volaille_Import / Volaille_Dispo_int)")
    ax.set_ylabel("Pays")
    ax.set_xlim(0, 1)
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    st.pyplot(fig)