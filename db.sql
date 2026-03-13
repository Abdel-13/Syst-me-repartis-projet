-- Script de création de la base de données pour le projet de supervision
-- Compatible avec SQLite ou MySQL

-- Table des machines (noeuds)
CREATE TABLE IF NOT EXISTS nodes (
    node_id VARCHAR(50) PRIMARY KEY, -- ID unique de l'agent [cite: 34]
    os_name VARCHAR(50),
    cpu_type VARCHAR(100),
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des métriques (historique)
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id VARCHAR(50),
    cpu_usage FLOAT, -- Charge CPU en % [cite: 35]
    mem_usage FLOAT, -- Charge mémoire en % [cite: 35]
    disk_usage FLOAT, -- Stockage disque en % [cite: 35]
    uptime INTEGER, -- Durée d'activité en secondes [cite: 36]
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes(node_id)
);

-- Table des services et ports
CREATE TABLE IF NOT EXISTS services_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id VARCHAR(50),
    service_name VARCHAR(50), -- 6 services (3 réseaux, 3 apps) [cite: 37]
    status VARCHAR(10), -- OK ou KO
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (node_id) REFERENCES nodes(node_id)
);

-- Table des alertes et logs
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id VARCHAR(50),
    event_type VARCHAR(50), -- Alerte seuil ou Panne [cite: 48]
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);