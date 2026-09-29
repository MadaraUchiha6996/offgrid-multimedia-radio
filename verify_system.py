import os
import sys
import sqlite3
import time

# Explicitly ensure your current folder path is visible to Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from packet import RadioPacket
    from network_env import VirtualRadioAirInterface
    from main_server import MasterOffGridServer
    from security import OffGridCipher
    from audio_codec import AudioStreamChunk
except ImportError as e:
    print(f"
 Error: Cannot find your project files. Make sure this script is saved inside the OffGridRadioServer folder! Details: {e}")
    sys.exit(1)

def run_comprehensive_verification():
    print("==================================================================")
    print("  OFF-GRID NETWORK END-TO-END VERIFICATION SEQUENCE INITIALIZED")
    print("==================================================================\n")

    # Step 1: Wipe clean old test database paths if they exist
    db_file = "live_radio_records.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception:
            pass

    # Step 2: Initialize Core Network Spaces
    print("[*] STEP 1: Booting Virtual Air Interface and Master Server...")
    air_interface = VirtualRadioAirInterface()
    server = MasterOffGridServer(node_id=1000, air_interface=air_interface)
    print("[+] Core Server Online.")

    # Step 3: Simulate Handset Outbound Encoding & Encrypted Transmission
    print("\n[*] STEP 2: Generating Secure Emergency Handset Telemetry...")
    cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
    
    secret_alert = "ALERT: Sector 4 Medical Hub operational on backup power banks."
    encrypted_payload = cipher.process_payload(secret_alert.encode('utf-8'))
    
    # Pack into raw binary structural frame
    packet = RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=201,  # Handset ID
        dest_node=1000,   # Server Target
        packet_id=88,
        ttl=4,
        flags=0x02,       # Mark as Encrypted
        payload=encrypted_payload
    )
    serialized_frame = packet.serialize()
    print(f"[+] Handset 201 packed message successfully ({len(serialized_frame)} bytes).")

    # Step 4: Fire Packet through the Air Space into the Server's Queue
    print("\n[*] STEP 3: Transmitting radio wave frame to the server...")
    air_interface.broadcast_packet(sender_id=201, raw_frame=serialized_frame)
    
    # Step 5: Force Server background tick cycle to ingest input buffers
    server.update()

    # Step 6: Query Persistent Storage to Verify Structural Data Integrity
    print("\n[*] STEP 4: Inspecting SQLite Database for secure record storage...")
    if not os.path.exists(db_file):
        print(" CRITICAL FAILURE: Database file was not created on disk.")
        sys.exit(1)

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT source_node, dest_node, message_text FROM text_messages WHERE packet_id = 88")
        row = cursor.fetchone()
        conn.close()

        if row:
            src, dest, text = row
            print("\n==================================================================")
            print(" [SUCCESS] DATA INTEGRITY VERIFIED - SERVER FUNCTIONAL!")
            print("==================================================================")
            print(f" • Retrieved Source ID : {src} (Matches Handset 201)")
            print(f" • Destination ID      : {dest} (Matches Server 1000)")
            print(f" • Safe Decoded Message: '{text}'")
            print("==================================================================\n")
        else:
            print(" FAILURE: SQL query executed but no matching message data rows were found.")
            sys.exit(1)

    except Exception as e:
        print(f" Database Validation Fault Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_comprehensive_verification()
