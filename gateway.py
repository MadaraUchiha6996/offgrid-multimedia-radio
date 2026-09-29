import sqlite3
import os
from datetime import datetime

VOICE_DIR = "voice_vault"
if not os.path.exists(VOICE_DIR):
    os.makedirs(VOICE_DIR)

def parse_incoming_radio_frame(raw_frame, rssi, snr):
    timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. FIXED: Added correct list-indexing brackets [1] and [0] to parse handshakes
    if "[SYS_INIT]" in raw_frame:
        try:
            sender_id = raw_frame.split("[SRC:")[1].split("]")[0]
        except IndexError:
            sender_id = "UNKNOWN"
            
        conn = sqlite3.connect("offgrid_network.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO tracked_peers (node_id, device_name, status, last_seen, last_rssi, last_snr)
            VALUES (?, ?, 'ONLINE', ?, ?, ?)
        ''', (sender_id, f"ESP32 Node #{sender_id}", timestamp_now, rssi, snr))
        conn.commit()
        conn.close()
        print(f"\n📡 [HANDSHAKE Check-In] Node {sender_id} synchronized automatically. Signal: {rssi} dBm")

    # 2. FIXED: Applied clean index array extractions to safely slice alphanumeric strings
    elif "[DST:" in raw_frame and "[V_NOTE:" not in raw_frame:
        try:
            sender = raw_frame.split("[SRC:")[1].split("]")[0]
            receiver = raw_frame.split("[DST:")[1].split("]")[0]
            message_body = raw_frame.split("] ")[-1]
        except IndexError:
            print(f"[PACKET FAULT] Dropping deformed link layer frame string: {raw_frame}")
            return

        conn = sqlite3.connect("offgrid_network.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO text_vault (timestamp, sender, receiver, message)
            VALUES (?, ?, ?, ?)
        ''', (timestamp_now, sender, receiver, message_body))
        conn.commit()
        conn.close()
        print(f"\n📨 [TEXT ARCHIVED] From: {sender} -> To: {receiver} | Content: \"{message_body}\"")

    # 3. FIXED: Added tracking element indices to handle memory note audio limits
    elif "[V_NOTE:" in raw_frame:
        try:
            sender = raw_frame.split(":#")[1].split(":")[0]
            expected_bytes = int(raw_frame.split(":")[-1].split("]")[0])
        except (IndexError, ValueError):
            print(f"[MEDIA FAULT] Fragmented voice payload initialization rejected.")
            return
            
        file_dest = os.path.join(VOICE_DIR, f"voice_{sender}_{int(datetime.now().timestamp())}.raw")
        
        conn = sqlite3.connect("offgrid_network.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO voice_ledger (timestamp, sender, file_size_bytes, file_path)
            VALUES (?, ?, ?, ?)
        ''', (timestamp_now, sender, expected_bytes, file_dest))
        conn.commit()
        conn.close()
        print(f"\n🎙️ [VOICE ROUTED] Stream open from Node #{sender}. Expecting: {expected_bytes} bytes -> Registered to /{file_dest}")

if __name__ == "__main__":
    print("[GATEWAY ROUTER] Standalone diagnostic frame translation layer loaded. Interface active.")
