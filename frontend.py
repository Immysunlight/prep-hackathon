import os  # accès aux variables d'environnement
import requests  # envoie des requêtes HTTP à ton API
import streamlit as st  # bibliothèque d'interface web
from dotenv import load_dotenv  # lit le fichier .env

load_dotenv()  # charge les variables du .env
API_URL = "http://127.0.0.1:8000"  # adresse de ton API FastAPI
HEADERS = {"x-api-key": os.getenv("API_KEY", "")}  # en-tête d'authentification (chaîne vide si la clé manque)

st.title("Mes items")  # titre affiché en haut de la page
titre = st.text_input("Titre")  # champ de saisie ; sa valeur est stockée dans la variable titre

if st.button("Ajouter"):  # ce bloc s'exécute quand on clique sur le bouton
    try:  # on tente d'appeler l'API
        r = requests.post(f"{API_URL}/items", json={"titre": titre}, headers=HEADERS, timeout=10)  # POST : envoie le titre en JSON avec la clé
        r.raise_for_status()  # lève une erreur si le code est 4xx ou 5xx
        st.success("Item ajouté")  # message vert de confirmation
    except requests.exceptions.RequestException as e:  # API éteinte, clé fausse, timeout...
        st.error(f"Erreur : {e}")  # message rouge avec le détail

try:  # on tente de charger la liste
    r = requests.get(f"{API_URL}/items", headers=HEADERS, timeout=10)  # GET : récupère tous les items
    r.raise_for_status()  # lève une erreur si le code est 4xx ou 5xx
    st.table(r.json())  # affiche la liste (id, titre) dans un tableau
except requests.exceptions.RequestException as e:  # même gestion d'erreur
    st.error(f"Impossible de charger les items : {e}")  # message rouge