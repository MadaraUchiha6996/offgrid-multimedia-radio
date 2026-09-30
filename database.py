import sqlite3

DB_FILE = "offgrid_network.db"


def init_vaults():
    # Context manager natively handles conn.commit() and conn.close()
    with sqlite3.connect(DB_FILE) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tracked_peers (
                node_id TEXT PRIMARY KEY, device_name TEXT, status TEXT DEFAULT 'ONLINE',
                last_seen TIMESTAMP, last_rssi REAL, last_snr REAL
            );
            CREATE TABLE IF NOT EXISTS text_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TIMESTAMP,
                sender TEXT, receiver TEXT, message TEXT
            );
            CREATE TABLE IF NOT EXISTS voice_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TIMESTAMP,
                sender TEXT, file_size_bytes INTEGER, file_path TEXT
            );
        """
        )
    print("Database vaults initialized successfully")


if __name__ == "__main__":
    init_vaults()
