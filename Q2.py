print("Début de l'analyse de vulnérabilités supplémentaires")

import requests
from bs4 import BeautifulSoup
import random
import string
from urllib.parse import urljoin

def fuzzing_formulaire(url):
    print(f"Fuzzing des formulaires pour {url}")
    
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()  # Vérifier si la requête a réussi
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return
    
    soup = BeautifulSoup(reponse.text, 'html.parser')
    formulaires = soup.find_all('form')
    
    for formulaire in formulaires:
        action = formulaire.get('action')
        action_url = urljoin(url, action) if action else url
        print(f"Formulaire trouvé : {action_url}")
        
        champs = formulaire.find_all('input')
        donnees = {}
        
        for champ in champs:
            nom = champ.get('name')
            if nom:
                # Génération de données aléatoires pour le fuzzing
                donnees[nom] = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=10))
        
        # Envoi du formulaire avec les données de fuzzing
        try:
            reponse_fuzzing = requests.post(action_url, data=donnees)
            print(f"Réponse du serveur : {reponse_fuzzing.status_code}")
            if reponse_fuzzing.status_code == 500:
                print("Vulnérabilité potentielle détectée : Erreur serveur 500")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du fuzzing : {e}")

# Exécution du fuzzing pour BWAPP et WordPress
fuzzing_formulaire("http://192.168.136.137/bWAPP/login.php")
fuzzing_formulaire("http://192.168.136.137/wordpress/")

print("L'analyse de vulnérabilités supplémentaires est terminée.")
