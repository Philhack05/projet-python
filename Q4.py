import paramiko
import psutil

def maintenir_acces_ssh(hostname, port, username, password, commande):
    # Création d'une instance de client SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)
    
    # Exécution de la commande pour maintenir l'accès
    stdin, stdout, stderr = client.exec_command(commande)
    result = stdout.read() + stderr.read()
    
    # Fermeture de la connexion
    client.close()
    return result

def collecter_infos_systeme():
    # Collecte des informations système sensibles
    infos_systeme = {
        "cpu_times": psutil.cpu_times(),
        "memory_stats": psutil.virtual_memory(),
        "disk_usage": psutil.disk_usage('/')
    }
    return infos_systeme

# Exemple d'utilisation
hostname = '192.168.136.137'
port = 22
username = 'root'
password = 'owaspbwa'
commande_ssh = 'echo "Reverse shell établi" > /tmp/reverse_shell.txt'

resultat_ssh = maintenir_acces_ssh(hostname, port, username, password, commande_ssh)
infos_systeme = collecter_infos_systeme()

print("Résultat de la commande SSH:", resultat_ssh)
print("Informations système collectées:", infos_systeme)
