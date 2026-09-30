import sqlite3

DB_FILE = "offgrid_network.db"

def init_vaults():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            sender TEXT,
            receiver TEXT,
            message TEXT
        )
    ''')
    
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
    print("Database vaults initialized successfully")

if __name__ == "__main__":
    init_vaults()
