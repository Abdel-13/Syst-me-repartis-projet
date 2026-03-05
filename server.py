import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor

# Configuration
HOST = '127.0.0.1'
PORT = 5000
MAX_WORKERS = 100  # Pool de threads


def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode('utf-8')
        if data:
            metrics = json.loads(data)
            # Affichage personnalisé avec l'ID de l'agent
            print(f"--- Données reçues de : {metrics['node_id']} ---")
            print(f"Statut : CPU {metrics['cpu_usage']}% | RAM {metrics['mem_usage']}%")
            print(f"Uptime : {metrics['uptime']}s")
            print("-" * 40)
    except Exception as e:
        print(f"[ERREUR] {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVEUR] En écoute sur {HOST}:{PORT}...")

    # Utilisation d'un Pool de threads (consigne projet)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            conn, addr = server.accept()
            executor.submit(handle_client, conn, addr)


if __name__ == "__main__":
    start_server()