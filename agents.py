import socket
import json
import sys
import subprocess
import time
import psutil
import platform

# Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000


def run_agent(agent_name):
    """Collecte et envoie les données au serveur"""
    try:
        # Collecte des métriques réelles
        data = {
            "node_id": agent_name,
            "os": platform.system(),
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent
        }

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        s.send(json.dumps(data).encode('utf-8'))
        s.close()
    except Exception as e:
        # En mode stress, on évite d'afficher 100 erreurs si le serveur est coupé
        pass


if __name__ == "__main__":
    # Cas 1 : Mode test de charge (100 agents dans l'ordre)
    if len(sys.argv) > 1 and sys.argv[1] == "connexion":
        print("--- Connexion ordonné de 100 agents (1 à 100) ---")
        for i in range(1, 101):
            agent_id = f"Agent-{i:03d}"
            subprocess.Popen(["python", "agents.py", agent_id])
            print(f"Connexion de {agent_id}...")
            time.sleep(0.1)  # Pause pour garantir l'ordre d'arrivée au serveur
        print("\nTerminé : Les 100 agents tournent en arrière-plan.")

    # Cas 2 : Un agent spécifique (ex: python agents.py MonPC)
    elif len(sys.argv) > 1:
        run_agent(sys.argv[1])

    # Cas 3 : Aide
    else:
        print("Usage: python agents.py connexion")
