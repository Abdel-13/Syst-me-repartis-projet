import sys
import socket
import json
import psutil
import platform
import time
from datetime import datetime

# Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
# Nous permet d'afficher plusieurs agents:
NODE_ID = sys.argv[1] if len(sys.argv) > 1 else "Agent-Defaut"

def get_metrics():
    # 1. Métriques de base [cite: 34, 35, 36]
    metrics = {
        "node_id": NODE_ID,
        "timestamp": datetime.now().isoformat(),
        "os": platform.system(),
        "cpu_type": platform.processor(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "mem_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "uptime": int(time.time() - psutil.boot_time()),
    }

    # 2. Alertes (Charge > 90%)
    if metrics["cpu_usage"] > 90 or metrics["mem_usage"] > 90:
        metrics["alert"] = "CRITICAL: High resource usage!"

    # 3. Services (3 réseaux, 3 apps) [cite: 37]
    # Note: On simule ou vérifie si le processus existe
    services = ['sshd', 'nginx', 'mysql', 'chrome', 'vlc', 'discord']
    metrics["services"] = {s: "OK" if s in [p.name() for p in psutil.process_iter()] else "KO" for s in services}

    # 4. Ports (4 prédéfinis) [cite: 38]
    ports = [22, 80, 443, 3306]
    metrics["ports"] = {}
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            metrics["ports"][port] = "OPEN" if s.connect_ex(('127.0.0.1', port)) == 0 else "CLOSED"

    return metrics


def run_agent():
    while True:
        try:
            data = get_metrics()
            # Connexion TCP [cite: 39]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((SERVER_IP, SERVER_PORT))
                client_socket.sendall(json.dumps(data).encode('utf-8'))
            print(f"[{data['timestamp']}] Données envoyées avec succès.")
        except Exception as e:
            print(f"Erreur de connexion : {e}")

        time.sleep(30)  # Fréquence d'envoi [cite: 74]


if __name__ == "__main__":
    run_agent()