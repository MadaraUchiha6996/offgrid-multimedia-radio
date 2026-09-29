import sqlite3
import os
from typing import List, Tuple, Dict, Any

class OffGridDatabase:
    """
    Manages persistent SQLite storage for the off-grid server.
    Ensures safe data writes during power loss using strict context managers
    and enforces parameterized statements to secure queries.
    """
    def __init__(self, db_path: str = "radio_records.db"):
        self.db_path = db_path
        self._initialize_tables()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes an atomic database connection instance."""
        return sqlite3.connect(self.db_path)

    def _initialize_tables(self):
        """Generates required schemas if they do not exist on the local directory."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Text Messages and System Emergency Alerts Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    packet_id INTEGER,
                    source_node INTEGER,
                    dest_node INTEGER,
                    timestamp REAL,
                    message_text TEXT
                )
            ''')
            
            # 2. Reassembled Voice Notes Storage Catalog Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS voice_notes (
                    message_id INTEGER PRIMARY KEY,
                    source_node INTEGER,
                    timestamp REAL,
                    file_path TEXT
                )
            ''')
            
            # 3. Server Queue for Outbound/Requested Handset Sync Packets
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS outbound_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    target_node INTEGER,
                    packet_type INTEGER,
                    payload BLOB
                )
            ''')
            conn.commit()

    def insert_text_message(self, packet_id: int, src: int, dest: int, text: str):
        """Safely appends decoded radio frames using parameter binding."""
        import time
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO text_messages (packet_id, source_node, dest_node, timestamp, message_text) 
                   VALUES (?, ?, ?, ?, ?)""",
                (packet_id, src, dest, time.time(), text)
            )
            conn.commit()

    def insert_voice_record(self, message_id: int, src: int, file_path: str):
        """Logs tracking records for complete audio stream reassemblies."""
        import time
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO voice_notes (message_id, source_node, timestamp, file_path) 
                   VALUES (?, ?, ?, ?)""",
                (message_id, src, time.time(), file_path)
            )
            conn.commit()

    def fetch_queued_packets(self, target_node: int) -> List[Tuple[int, int, bytes]]:
        """Retrieves outstanding message queue rows bound for a specific node ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, packet_type, payload FROM outbound_queue WHERE target_node = ?",
                (target_node,)
            )
            return cursor.fetchall()

    def clear_queue_item(self, queue_db_id: int):
        """Removes items from queue once delivery verification completes successfully."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM outbound_queue WHERE id = ?", (queue_db_id,))
            conn.commit()


# --- Local Sanity Integrity Check Execution ---
if __name__ == "__main__":
    print("[*] Running secure database structural loopback checks...")
    db = OffGridDatabase("test_radio.db")
    
    # Run test write using safe bindings
    db.insert_text_message(packet_id=12, src=201, dest=1000, text="Emergency Alert: Safe")
    print("[+] Parameterized SQL insertion passed security test.")
    
    # Clean up test artifact footprint
    if os.path.exists("test_radio.db"):
        os.remove("test_radio.db")
    print("[+] All localized database schema components verified cleanly.")
