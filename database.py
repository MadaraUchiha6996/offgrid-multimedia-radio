import sqlite3
from datetime import datetime

DB_FILE = "offgrid_network.db"

def init_vaults():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Matches Option 3: Track active peer nodes and computed RSSI distances
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracked_peers (
            node_id TEXT PRIMARY KEY,
            device_name TEXT,
            status TEXT DEFAULT 'ONLINE',
            last_seen TIMESTAMP,
            last_rssi REAL,
            last_snr REAL
        )
    ''')
    
    # Matches Option 1 & 2: Alphanumeric secure text vault records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            sender TEXT,
            receiver TEXT,
            message TEXT
        )
    ''')
    
    # Matches Option 2 (Voice Note Archives Request Module)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voice_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            sender TEXT,
            file_size_bytes INTEGER,
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("[SERVER DB] Core SQLite asset vaults matching handheld firmware initialized.")

if __name__ == "__main__":
    init_vaults()
