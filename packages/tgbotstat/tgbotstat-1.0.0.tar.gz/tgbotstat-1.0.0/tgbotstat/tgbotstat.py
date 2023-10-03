"""
$$$$$$$$\        $$\                  $$\                 $$\                $$\     
\__$$  __|       $$ |                 $$ |                $$ |               $$ |    
   $$ | $$$$$$\  $$$$$$$\   $$$$$$\ $$$$$$\    $$$$$$$\ $$$$$$\    $$$$$$\ $$$$$$\   
   $$ |$$  __$$\ $$  __$$\ $$  __$$\\_$$  _|  $$  _____|\_$$  _|   \____$$\\_$$  _|  
   $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ | $$ |    \$$$$$$\    $$ |     $$$$$$$ | $$ |    
   $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ | $$ |$$\  \____$$\   $$ |$$\ $$  __$$ | $$ |$$\ 
   $$ |\$$$$$$$ |$$$$$$$  |\$$$$$$  | \$$$$  |$$$$$$$  |  \$$$$  |\$$$$$$$ | \$$$$  |
   \__| \____$$ |\_______/  \______/   \____/ \_______/    \____/  \_______|  \____/ 
       $$\   $$ |                                                                    
       \$$$$$$  |                                                                    
        \______/                                                                                                                                                                                          
"""
import os
import json
from datetime import date

# NOM DES FICHIERS STATISTIQUES
fichier_statistiques = 'statistiques.json'
fichier_utilisateurs = 'utilisateurs.txt'

# ICI JE VERIFIE SI LES FICHIER SONT CREES, SI OUI JE PASSE
if not os.path.exists(fichier_statistiques):
    with open(fichier_statistiques, 'w') as fichier:
        json.dump({'commands': {}}, fichier)

if not os.path.exists(fichier_utilisateurs):
    open(fichier_utilisateurs, 'w').close()

def charger_statistiques():
    try:
        with open(fichier_statistiques, 'r') as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return {'commands': {}}

def sauvegarder_statistiques(statistiques):
    with open(fichier_statistiques, 'w') as fichier:
        json.dump(statistiques, fichier, indent=2)

# ALGO POUR METTRE A JOUR LE STATISTIQUE DES INTERACTIONS DE COMMANDES
def mettre_a_jour_statistiques_commande(statistiques, commande, id_utilisateur, heure_commande, jour_semaine):
    aujourd_hui = date.today().isoformat()
    if aujourd_hui not in statistiques['commands']:
        statistiques['commands'][aujourd_hui] = {}
    if commande not in statistiques['commands'][aujourd_hui]:
        statistiques['commands'][aujourd_hui][commande] = {'nombre_utilisations': 0, 'utilisateurs': []}

    statistiques['commands'][aujourd_hui][commande]['nombre_utilisations'] += 1
    if id_utilisateur not in statistiques['commands'][aujourd_hui][commande]['utilisateurs']:
        statistiques['commands'][aujourd_hui][commande]['utilisateurs'].append(id_utilisateur)

    # Enregistrement de l'heure de la commande
    if 'heures' not in statistiques['commands'][aujourd_hui][commande]:
        statistiques['commands'][aujourd_hui][commande]['heures'] = {}
    if heure_commande not in statistiques['commands'][aujourd_hui][commande]['heures']:
        statistiques['commands'][aujourd_hui][commande]['heures'][heure_commande] = 1
    else:
        statistiques['commands'][aujourd_hui][commande]['heures'][heure_commande] += 1

    sauvegarder_statistiques(statistiques)

def charger_utilisateurs():
    with open(fichier_utilisateurs, 'r') as fichier:
        return fichier.read().splitlines()

def enregistrer_utilisateur(id_utilisateur):
    with open(fichier_utilisateurs, 'a') as fichier:
        fichier.write(str(id_utilisateur) + '\n')

def suivre_commandes_populaires(statistiques, commande):
    if "commandes_populaires" not in statistiques:
        statistiques["commandes_populaires"] = {}
    if commande not in statistiques["commandes_populaires"]:
        statistiques["commandes_populaires"][commande] = 1
    else:
        statistiques["commandes_populaires"][commande] += 1
    sauvegarder_statistiques(statistiques)