from jinja2 import Environment, FileSystemLoader
import datetime
import matplotlib.pyplot as plt
import os

# Exemple de données de vulnérabilités
vulnerabilities = [
    {'service': 'HTTP', 'port': 80, 'description': 'Injection SQL', 'severity': 'High'},
    {'service': 'SSH', 'port': 22, 'description': 'Faiblesse d\'authentification', 'severity': 'Medium'},
    {'service': 'FTP', 'port': 21, 'description': 'Mot de passe faible', 'severity': 'Critical'},
]

def generate_html_report(target, vulnerabilities, graph_path):
    # Définir le chemin absolu du dossier contenant le template
    template_dir = '/home/torodo/Bureau/templates'
    env = Environment(loader=FileSystemLoader(template_dir))

    try:
        template = env.get_template('template.html')
    except Exception as e:
        print(f"Erreur lors du chargement du template : {e}")
        return

    # Contexte à passer au template
    context = {
        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'target': target,
        'vulnerabilities': vulnerabilities,
        'graph_path': graph_path
    }

    # Générer le rendu HTML
    try:
        html_content = template.render(context)
    except Exception as e:
        print(f"Erreur lors du rendu du template : {e}")
        return
    
    # Sauvegarder le rapport
    report_file_path = 'rapport_securite.html'
    try:
        with open(report_file_path, 'w') as report_file:
            report_file.write(html_content)
        print(f"Rapport généré : {report_file_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du rapport : {e}")

def generate_vulnerability_graph(vulnerabilities):
    # Extraire les données pour le graphique
    severities = [vuln['severity'] for vuln in vulnerabilities]

    # Compter les occurrences de chaque sévérité
    severity_levels = ['Low', 'Medium', 'High', 'Critical']
    severity_count = {level: severities.count(level) for level in severity_levels}

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.bar(severity_count.keys(), severity_count.values(), color=['green', 'orange', 'red', 'darkred'])
    plt.title('Distribution des Vulnérabilités par Sévérité')
    plt.xlabel('Sévérité')
    plt.ylabel('Nombre de Vulnérabilités')
    plt.grid(axis='y')

    # Sauvegarder le graphique
    graph_path = 'vulnerabilities_graph.png'
    try:
        plt.savefig(graph_path)
        print(f"Graphique généré : {graph_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du graphique : {e}")
    plt.close()

    return graph_path

# Générer le graphique
graph_path = generate_vulnerability_graph(vulnerabilities)

# Générer le rapport HTML
generate_html_report('192.168.136.137', vulnerabilities, graph_path)

