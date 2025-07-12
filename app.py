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
    return pd.read_csv("df_kmeans_0_3.csv")

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

    # Bloc 1 - Part de terre bio
    st.subheader("Part de terre bio")
    top_10_bio = df[['Pays', 'Part_terre_bio']].sort_values(by='Part_terre_bio', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(top_10_bio['Pays'], top_10_bio['Part_terre_bio'], color='green')
    ax.set_title("Top 10 pays par part de terres bio")
    ax.set_xlabel("Part de terres agricoles en bio (%)")
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Bloc 2 - Indice de dépendance bio
    st.subheader("Indice de dépendance bio")
    df["Indice_dépendance_bio"] = df["Part_terre_bio"] / df["Volaille_Import"]
    top10_dependance_bio = df[['Pays', 'Indice_dépendance_bio']].sort_values(by='Indice_dépendance_bio', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top10_dependance_bio['Pays'], top10_dependance_bio['Indice_dépendance_bio'], color='seagreen')
    ax.set_title("Top 10 - Indice de dépendance bio")
    ax.set_ylabel("Indice de dépendance bio")
    ax.set_xticklabels(top10_dependance_bio['Pays'], rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Bloc 3 - Bio par crédit
    st.subheader("Part de terre bio par crédit")
    df["Bio_par_crédit"] = df["Part_terre_bio"] / df["Credit_total"]
    top10_bio_credit = df[['Pays', 'Bio_par_crédit']].sort_values(by='Bio_par_crédit', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(top10_bio_credit['Pays'], top10_bio_credit['Bio_par_crédit'], color='teal')
    ax.set_title("Top 10 - Part de terre bio par crédit")
    ax.set_xlabel("Bio par crédit")
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Bloc 4 - Dépendance aux importations volaille
    st.subheader("Dépendance aux importations de volaille")
    df["Ratio_import_volaille"] = df["Volaille_Import"] / df["Volaille_Dispo_int"]
    top10_import_volaille = df[['Pays', 'Ratio_import_volaille']].sort_values(by='Ratio_import_volaille', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(top10_import_volaille['Pays'], top10_import_volaille['Ratio_import_volaille'], color='orange', edgecolor='black')
    ax.set_title("Top 10 - Dépendance aux importations de volaille")
    ax.set_xlabel("Ratio Import / Disponibilité intérieure")
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

elif choice == "Classement global":
    st.header("\U0001F3C6 Classement des pays les plus présents dans les Top 10")
    listes_top10 = [
        df[['Pays', 'Part_terre_bio']].sort_values(by='Part_terre_bio', ascending=False).head(10)['Pays'].tolist(),
        df[['Pays', 'Ratio_import_volaille']].sort_values(by='Ratio_import_volaille', ascending=False).head(10)['Pays'].tolist(),
        df[['Pays', 'Indice_dépendance_bio']].sort_values(by='Indice_dépendance_bio', ascending=False).head(10)['Pays'].tolist(),
        df[['Pays', 'Bio_par_crédit']].sort_values(by='Bio_par_crédit', ascending=False).head(10)['Pays'].tolist(),
        df[df["Indice_betail"] > 100].assign(Volaille_import_vs_betail = lambda x: x["Volaille_Import"] / x["Indice_betail"]).sort_values(by="Volaille_import_vs_betail", ascending=False).head(10)['Pays'].tolist(),
        df[(df["Indice_betail"] < 100) & (df["Pays"] != "FRANCE")].sort_values(by="Volaille_Import", ascending=False).head(10)['Pays'].tolist()
    ]
    tous_les_pays = [p for l in listes_top10 for p in l]
    compte_pays = pd.Series(tous_les_pays).value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(compte_pays.index, compte_pays.values, color='steelblue', edgecolor='black')
    ax.set_title("Pays les plus présents dans les top 10 stratégiques")
    ax.set_xlabel("Nombre d'apparitions dans les top 10")
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

elif choice == "Import vs cheptel":
    st.header("\U0001F413 Pays avec cheptel développé mais forte dépendance à l'import")
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
    df_top_import = df_betail_bas.sort_values(by="Volaille_Import", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_top_import, y="Pays", x="Volaille_Import", palette="crest", edgecolor="black", ax=ax)
    ax.set_title("Pays à cheptel limité mais forte importation de volaille")
    ax.set_xlabel("Importation de volaille")
    ax.set_ylabel("Pays")
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

elif choice == "Conclusion":
    st.header("📝 Conclusion")

    st.markdown("""
    ## ✈️ Exportation

    **Le choix porte sur :**  
    - 🇧🇪 **Belgique**  
    - 🇳🇱 **Pays-Bas**  
    - 🌍 ou 🇿🇦 **Afrique du Sud** *(option internationale)*

    Ces pays bénéficient d’avantages significatifs :  
    une **forte dépendance aux importations**, une **consommation soutenue**,  
    et un **marché local mature**, bien **connecté aux réseaux de transport mondiaux**.

    ---

    ## 🏭 Implantation locale

    **Le choix porte sur :**  
    - 🇨🇿 **République Tchèque**  
    - 🇮🇹 **Italie**  
    - 🌍 ou 🇦🇺 **Australie** *(option internationale)*

    Ces marchés sont des **terres d’accueil favorables à la culture du bio**.  
    La **part de terres bio y est importante**, **l’activité est soutenue par les gouvernements locaux**,  
    et **l’investissement dans le bio semble rentable à long terme**.
    """)