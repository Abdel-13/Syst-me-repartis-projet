import socket
import json
import sqlite3
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configuration
HOST = '127.0.0.1'
PORT = 5000
DB_NAME = "supervision.db"


class SQLitePool:
    def __init__(self, db_name):
        self.db_name = db_name

    # Ici, on définit 6 arguments (self + 5 données)
    def update_node_and_metrics(self, node_id, os, cpu_type, cpu_val, ram_val, last_seen):
        conn = sqlite3.connect(self.db_name)
        try:
            cursor = conn.cursor()

            # Table 'nodes' : 4 colonnes (node_id, os_name, cpu_type, last_seen)
            cursor.execute("""
                INSERT OR REPLACE INTO nodes (node_id, os_name, cpu_type, last_seen) 
                VALUES (?, ?, ?, ?)""",
                           (node_id, os, cpu_type, last_seen))

            # Table 'metrics' : Pour l'historique (node_id, cpu_usage, mem_usage, timestamp)
            cursor.execute("""
                INSERT INTO metrics (node_id, cpu_usage, mem_usage, timestamp) 
                VALUES (?, ?, ?, ?)""",
                           (node_id, cpu_val, ram_val, last_seen))

            conn.commit()
        finally:
            conn.close()

    def update_node(self, node_id, m, last_seen):
        conn = sqlite3.connect(self.db_name)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?)",
                           (node_id, m, last_seen))
            conn.commit()
        finally:
            conn.close()


def handle_client(conn, addr, db_pool):
    try:
        raw_data = conn.recv(4096).decode('utf-8')
        if not raw_data: return
        m = json.loads(raw_data)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # On envoie exactement 6 arguments (en comptant self qui est automatique)
        db_pool.update_node_and_metrics(
            m['node_id'],
            m['os'],
            m.get('cpu_type', 'Inconnu'),
            m['cpu'],
            m['ram'],
            now
        )

        #Afficher le CPU et le RAM :
        print(f"[{now}] {m['node_id']} connecté | CPU: {m['cpu']}% | RAM: {m['ram']}%")

    except Exception as e:
        print(f"Erreur client {addr}: {e}")
    finally:
        conn.close()


def start_server():
    db_pool = SQLitePool(DB_NAME)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"SERVEUR ACTIF sur {HOST}:{PORT}...")

        with ThreadPoolExecutor(max_workers=15) as pool:
            while True:
                conn, addr = server.accept()
                pool.submit(handle_client, conn, addr, db_pool)
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
