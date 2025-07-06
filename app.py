import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Config Streamlit
st.set_page_config(layout="wide", page_title="Analyse Exportation Volaille Bio")
st.title("\U0001F4C4 Présentation de l'étude")

st.markdown("""
### Étude sur le développement commercial à l'international pour la société française *La Poule qui chante*.

Cette étude repose sur une sélection de variables **macroéconomiques** et **sectorielles** (secteur de la **volaille bio**) afin d'identifier un pays avec lequel **initier une relation commerciale** : implantation physique ou échange de flux commerciaux.
""")

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("df_filtre_median.csv")

df = load_data()

st.sidebar.title("Navigation")
options = [
    "Top 10 par indicateur",
    "Classement global",
    "Import vs cheptel",
    "Dépendance avec cheptel < 100",
    "Conclusion"
]
choice = st.sidebar.radio("Aller vers...", options)

if choice == "Top 10 par indicateur":
    st.header("\U0001F4CA Top 10 par indicateur")

    # Part de terre bio
    st.subheader("Part de terre bio")
    top_10_bio = df[['Pays', 'Part_terre_bio']].sort_values(by='Part_terre_bio', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=top_10_bio, x='Part_terre_bio', y='Pays', ax=ax)
    ax.set_title("Top 10 - Part de terre bio")
    st.pyplot(fig)

    # Indice de dépendance bio
    st.subheader("Indice de dépendance bio")
    top10_dependance_bio = df[['Pays', 'Indice_dépendance_bio']].sort_values(by='Indice_dépendance_bio', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=top10_dependance_bio, x='Indice_dépendance_bio', y='Pays', ax=ax, color='seagreen')
    ax.set_title("Top 10 - Indice de dépendance bio")
    st.pyplot(fig)

    # Bio par crédit
    st.subheader("Part de terre bio par crédit")
    top10_bio_credit = df[['Pays', 'Bio_par_crédit']].sort_values(by='Bio_par_crédit', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=top10_bio_credit, x='Bio_par_crédit', y='Pays', ax=ax, color='teal')
    ax.set_title("Top 10 - Part de terre bio par crédit")
    st.pyplot(fig)

    # Ratio import volaille
    st.subheader("Dépendance aux importations de volaille")
    top10_import_volaille = df.sort_values(by='Ratio_import_volaille', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=top10_import_volaille, x='Ratio_import_volaille', y='Pays', ax=ax)
    ax.set_title("Top 10 - Dépendance aux importations de volaille")
    st.pyplot(fig)

elif choice == "Classement global":
    st.header("\U0001F3C6 Classement des pays les plus performants")
    indicateurs = [
        "Part_terre_bio",
        "Indice_dépendance_bio",
        "Bio_par_crédit",
        "Volaille_import_vs_betail",
        "Ratio_import_volaille"
    ]
    apparitions_top10 = {}
    for indicateur in indicateurs:
        top10 = df.sort_values(by=indicateur, ascending=False).head(10)
        for pays in top10['Pays']:
            apparitions_top10[pays] = apparitions_top10.get(pays, 0) + 1
    df_presence = pd.DataFrame.from_dict(apparitions_top10, orient='index', columns=["Présence_top10"]).reset_index().rename(columns={'index': 'Pays'})
    df_presence = df_presence.sort_values(by="Présence_top10", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=df_presence, x="Présence_top10", y="Pays", ax=ax, palette="viridis")
    ax.set_title("Classement global - Nombre de présence dans les Top 10")
    st.pyplot(fig)

elif choice == "Import vs cheptel":
    st.header("\U0001F413 Pays avec cheptel développé mais forte dépendance ")
    df_betail = df[df["Indice_betail"] > 100].copy()
    df_betail["Volaille_import_vs_betail"] = df_betail["Volaille_Import"] / df_betail["Indice_betail"]
    top10 = df_betail.sort_values(by="Volaille_import_vs_betail", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=top10, x="Volaille_import_vs_betail", y="Pays", ax=ax, color="tomato")
    ax.set_title("Top 10 - Dépendants à l'import malgré un cheptel développé")
    st.pyplot(fig)

elif choice == "Dépendance avec cheptel < 100":
    st.header("\U0001F414 Importations dans les pays à faible cheptel")
    df_betail_bas = df[(df["Indice_betail"] < 100) & (df["Pays"] != "FRANCE")].copy()
    top10 = df_betail_bas.sort_values(by="Volaille_Import", ascending=False).head(10)
    top10["Classement"] = range(1, 11)
    st.dataframe(top10[["Classement", "Pays", "Indice_betail", "Volaille_Import"]])

elif choice == "Conclusion":
    st.header("\U0001F4DD Conclusion")
    st.markdown("""
    ### Au vu des analyses menées, nous pouvons conclure :

    - 