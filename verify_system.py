import os
import sys
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from packet import RadioPacket
    from network_env import VirtualRadioAirInterface
    from main_server import MasterOffGridServer
    from security import OffGridCipher
    from audio_codec import AudioStreamChunk
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

def run_comprehensive_verification():
    db_file = "live_radio_records.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception:
            pass

    air_interface = VirtualRadioAirInterface()
    server = MasterOffGridServer(node_id=1000, air_interface=air_interface)

    cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
    secret_alert = "ALERT: Sector 4 Medical Hub operational on backup power banks."
    encrypted_payload = cipher.process_payload(secret_alert.encode('utf-8'))
    
    packet = RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=201,  
        dest_node=1000,   
        packet_id=88,
        ttl=4,
        flags=0x02,       
        payload=encrypted_payload
    )
    serialized_frame = packet.serialize()

    air_interface.broadcast_packet(sender_id=201, raw_frame=serialized_frame)
    server.update()

    if not os.path.exists(db_file):
        print("Failure: No database file found")
        sys.exit(1)

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT source_node, dest_node, message_text FROM text_messages WHERE packet_id = 88")
        row = cursor.fetchone()
        conn.close()

        if row:
            src, dest, text = row
            print("Success")
        else:
            print("Failure: No row matches")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_comprehensive_verification()
