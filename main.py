import os  # accès aux variables d'environnement
import sqlite3  # base de données SQLite, incluse dans Python
from dotenv import load_dotenv  # lit le fichier .env
from fastapi import Depends, FastAPI, Header, HTTPException  # outils FastAPI
from pydantic import BaseModel  # valide le format des données reçues

load_dotenv()  # charge les variables du fichier .env
API_KEY = os.getenv("API_KEY")  # clé attendue des clients (None si absente)
DB = "app.db"  # nom du fichier de base de données

app = FastAPI()  # crée l'application API

def init_db():  # crée la table au démarrage
    with sqlite3.connect(DB) as conn:  # ouvre (ou crée) le fichier app.db
        conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, titre TEXT NOT NULL)")  # table items : id auto + titre

init_db()  # exécute la création de table

def verifier_cle(x_api_key: str = Header(None)):  # lit l'en-tête "x-api-key" de la requête
    if not API_KEY or x_api_key != API_KEY:  # clé absente côté serveur, ou fausse côté client
        raise HTTPException(status_code=401, detail="Clé d'API invalide")  # refuse avec un 401

class Item(BaseModel):  # format attendu pour créer un item
    titre: str  # un seul champ : le titre (texte)

@app.post("/items")  # route POST : créer un item
def creer_item(item: Item, _=Depends(verifier_cle)):  # Depends : la clé est vérifiée avant tout
    with sqlite3.connect(DB) as conn:  # ouvre la base
        cur = conn.execute("INSERT INTO items (titre) VALUES (?)", (item.titre,))  # insère ; le ? évite les injections SQL
        return {"id": cur.lastrowid, "titre": item.titre}  # renvoie l'item créé

@app.get("/items")  # route GET : lister les items
def lister_items(_=Depends(verifier_cle)):  # clé vérifiée aussi ici
    with sqlite3.connect(DB) as conn:  # ouvre la base
        lignes = conn.execute("SELECT id, titre FROM items").fetchall()  # lit toutes les lignes
    return [{"id": i, "titre": t} for i, t in lignes]  # convertit en liste de dictionnaires JSON