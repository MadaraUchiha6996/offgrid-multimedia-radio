import os
import sqlite3
import sys

# Core standard library environment setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio_codec import AudioStreamChunk
from main_server import MasterOffGridServer
from network_env import VirtualRadioAirInterface
from packet import RadioPacket
from security import OffGridCipher


def run_comprehensive_verification():
    db_file = "live_radio_records.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception:
            pass

    air = VirtualRadioAirInterface()
    server = MasterOffGridServer(node_id=1000, air_interface=air)

    # Inline packet construction and scheduling lifecycle
    encrypted = OffGridCipher("DelhiOffGridEmergencyNetwork2026").process_payload(
        b"ALERT: Sector 4 Medical Hub operational on backup power banks."
    )
    packet = RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=201,
        dest_node=1000,
        packet_id=88,
        ttl=4,
        flags=0x02,
        payload=encrypted,
    )

    air.broadcast_packet(sender_id=201, raw_frame=packet.serialize())
    server.update()

    if not os.path.exists(db_file):
        sys.exit(print("Failure: No database file found") or 1)

    # Unified database state validation
    with sqlite3.connect(db_file) as conn:
        row = conn.execute(
            "SELECT source_node, dest_node, message_text FROM text_messages WHERE packet_id = 88"
        ).fetchone()

    print("Success" if row else "Failure: No row matches")
    if not row:
        sys.exit(1)


if __name__ == "__main__":
    run_comprehensive_verification()
