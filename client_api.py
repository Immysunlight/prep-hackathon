import os  # accès aux variables d'environnement
import time  # pour faire une pause entre deux tentatives
import requests  # bibliothèque pour envoyer des requêtes HTTP
from dotenv import load_dotenv  # outil qui lit le fichier .env

load_dotenv()  # charge les variables du fichier .env
TOKEN = os.getenv("GITHUB_TOKEN")  # récupère le token (None s'il manque)

def appeler_api(url, token, essais=3):  # fonction réutilisable ; 3 tentatives maximum
    entetes = {"Authorization": f"Bearer {token}"}  # en-tête qui transporte le token
    for essai in range(1, essais + 1):  # boucle : essai 1, 2, puis 3
        try:  # on tente l'appel
            r = requests.get(url, headers=entetes, timeout=10)  # GET avec abandon après 10 s
        except requests.exceptions.RequestException as e:  # panne réseau ou timeout
            print(f"Réseau KO (essai {essai}) :", e)  # affiche l'erreur
            time.sleep(2 * essai)  # attend 2 s, puis 4 s, puis 6 s avant de réessayer
            continue  # passe à l'essai suivant
        if r.status_code == 200:  # succès
            return r.json()  # renvoie les données sous forme de dictionnaire
        if r.status_code == 401:  # token absent, faux ou expiré
            print("401 : vérifie ton token")  # inutile de réessayer
            return None  # abandon immédiat
        if r.status_code == 403:  # accès refusé ou quota dépassé
            print("403 : accès refusé ou quota dépassé")  # inutile de réessayer
            return None  # abandon immédiat
        if r.status_code == 404:  # adresse ou ressource introuvable
            print("404 : vérifie l'adresse (URL)")  # inutile de réessayer
            return None  # abandon immédiat
        if r.status_code == 429 or r.status_code >= 500:  # trop de requêtes ou panne du serveur
            print(f"{r.status_code} : serveur occupé, nouvel essai {essai}")  # affiche le code
            time.sleep(2 * essai)  # pause avant de réessayer
            continue  # passe à l'essai suivant
        print("Code inattendu :", r.status_code)  # tout autre code
        return None  # abandon

    print("Abandon après plusieurs essais")  # les 3 essais ont échoué
    return None  # rien à renvoyer

if __name__ == "__main__":  # s'exécute seulement quand on lance ce fichier directement
    profil = appeler_api("https://api.github.com/user/INCONNU", TOKEN)  # appel de test
    if profil:  # si on a bien reçu des données
        print("OK :", profil["login"])  # affiche ton pseudo