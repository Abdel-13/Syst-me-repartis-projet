Projet Final: Systèmes Répartis
Description: ce projet implémente un système de supervision basé sur une architecture Client-Serveur en Python.
 * * Agents (clients): Collectent les métriques (CPU, RAM, Disque, Services) et les envoients via sockets TCP.
 * * Serveur: Gère plusieurs clients simultanément grace à un pool de threads, valide les données et les stocks dans une base de données.

   Prérequis :
   - Python 3.10
   - Binliothéque "psutil" pour la collecte des métriques réels
   - SDLite3 est inclus par défaut avec Phyton
  
   Structure du Projet:
    - agent.py: C'est le scipt à exécuter sur chaque machine à superviser;
    - server.py: Le script central recevant les données;
    - db.sql: c'est le script de création de la base de données.
    - rapport.pdf: Résumé technique du projet.
  
   Installation et le lancement

   1- Préparation du serveur, agent et la base de données.
   2- Démarrage du serveur : On lance le serveur avec "python server.py"
   3- Démarrage des agents : avec le commandes "pyton agent.py Connexion"
