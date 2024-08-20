print("Début de la phase de collecte d'informations")

# Importation des bibliothèques nécessaires
import requests
from bs4 import BeautifulSoup, Comment
import re
from urllib.parse import urljoin

def collecter_informations(url):
    print(f"Collecte d'informations pour {url}")
    
    try:
        # Récupération de la page web
        reponse = requests.get(url)
        reponse.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        soup = BeautifulSoup(reponse.text, 'html.parser')
        
        # Extraction des formulaires
        formulaires = soup.find_all('form')
        print(f"Nombre de formulaires trouvés : {len(formulaires)}")
        
        # Extraction des liens
        liens = soup.find_all('a')
        print(f"Nombre de liens trouvés : {len(liens)}")
        
        # Extraction des scripts JavaScript
        scripts = soup.find_all('script')
        print(f"Nombre de scripts JavaScript trouvés : {len(scripts)}")
        
        # Extraction des commentaires HTML
        commentaires = soup.find_all(string=lambda text: isinstance(text, Comment))
        print(f"Nombre de commentaires HTML trouvés : {len(commentaires)}")
        
        # Extraction des méta-informations
        meta_tags = soup.find_all('meta')
        print(f"Nombre de balises meta trouvées : {len(meta_tags)}")
        
        # Recherche de points d'entrée potentiels (ex: paramètres GET)
        parametres_get = re.findall(r'\?(\w+)=', str(soup))
        print(f"Nombre de paramètres GET potentiels trouvés : {len(set(parametres_get))}")

        # Extraction des technologies utilisées
        technologies = []
        if soup.find(attrs={"name": "generator"}):
            technologies.append(soup.find(attrs={"name": "generator"})['content'])
        print(f"Technologies détectées : {', '.join(technologies)}")

        # Recherche de fichiers sensibles
        fichiers_sensibles = ['/robots.txt', '/sitemap.xml', '/.htaccess', '/wp-config.php', '/config.php']
        for fichier in fichiers_sensibles:
            url_fichier = urljoin(url, fichier)
            reponse = requests.head(url_fichier)
            if reponse.status_code == 200:
                print(f"Fichier sensible trouvé : {url_fichier}")

    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de {url} : {e}")

# Exécution de la collecte d'informations pour BWAPP et WordPress
collecter_informations("http://192.168.136.137/bWAPP/portal.php")
collecter_informations("http://192.168.136.137/wordpress/")

print("La phase de collecte d'informations est terminée.")

# Phase 2 : Analyse de vulnérabilités

print("Début de la phase d'analyse de vulnérabilités")

import nmap

def analyser_vulnerabilites(ip):
    print(f"Analyse des vulnérabilités pour {ip}")
    
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-sV --script vuln')
        
        for host in nm.all_hosts():
            print(f"Hôte : {host}")
            for proto in nm[host].all_protocols():
                print(f"Protocole : {proto}")
                ports = nm[host][proto].keys()
                for port in ports:
                    print(f"Port : {port}")
                    print(f"État : {nm[host][proto][port]['state']}")
                    print(f"Service : {nm[host][proto][port]['name']}")
                    if 'script' in nm[host][proto][port]:
                        for script in nm[host][proto][port]['script']:
                            print(f"Script : {script}")
                            print(f"Résultat : {nm[host][proto][port]['script'][script]}")

    except nmap.PortScannerError as e:
        print(f"Erreur lors de l'analyse des vulnérabilités pour {ip} : {e}")

# Exécution de l'analyse de vulnérabilités pour BWAPP et WordPress
analyser_vulnerabilites("adresse_ip_bwapp")
analyser_vulnerabilites("adresse_ip_wordpress")

print("La phase d'analyse de vulnérabilités est terminée.")

# Les phases suivantes (Exploitation, Post-exploitation et Reporting) nécessiteraient plus de détails et de contexte spécifique pour être implémentées de manière sûre et éthique.

print("Les phases d'Exploitation, Post-exploitation et Reporting nécessitent une analyse plus approfondie et des autorisations spécifiques.")

