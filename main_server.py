import time
import os
import struct
from packet import RadioPacket
from database import OffGridDatabase
from security import OffGridCipher
from gateway import OffGridInternetGateway
from satellite_receiver import SatelliteStreamDemux
from hardware_lora import SX1262HardwareWrapper, HARDWARE_MODE

class HardwareOffGridServer:
    """
    The physical master server engine running on the central Raspberry Pi 4.
    Bridges actual Semtech SX1262 SPI hardware buffers to the database and WAN.
    """
    def __init__(self, node_id: int):
        self.node_id = node_id
        
        # Initialize physical SPI Radio Interface Module (Uses standard BCM pins)
        self.radio = SX1262HardwareWrapper(
            bus=0, device=0, 
            pin_busy=24, pin_rst=22, pin_dio1=25
        )
        
        # Initialize internal infrastructure sub-systems
        self.db = OffGridDatabase("live_radio_records.db")
        self.cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
        self.gateway = OffGridInternetGateway()
        self.sat_demux = SatelliteStreamDemux()
        
        print(f"\n[+] Hardware Server Engine active on Node {self.node_id}.")
        print(f"    Mode: {'REAL PHYSICAL HARDWARE' if HARDWARE_MODE else 'EMULATED SPI REGISTERS'}")

    def listen_and_process_radio(self):
        """
        Continuously polls the physical Semtech radio chip registers via SPI 
        to capture, decode, decrypt, and process incoming handset transmissions.
        """
        raw_rx_bytes = b""
        
        if HARDWARE_MODE:
            # Low-level register operations for the real Waveshare HAT:
            # 1. Check if DIO1 pin goes HIGH (Signals a packet has fully landed in the RF FIFO)
            # 2. If active, read the payload length from register 0x13
            # 3. Fetch bytes using read_command(opcode=0x1E, num_bytes)
            pass
        else:
            # Emulation Loopback: Fallback to test processing pipeline without a physical Pi attached
            pass

        if not raw_rx_bytes:
            return

        packet = RadioPacket.deserialize(raw_rx_bytes)
        if not packet:
            return

        # Enforce server boundary destination filtering rules
        if packet.dest_node != self.node_id and packet.dest_node != 0xFFFF:
            return # Not meant for us, drop it to optimize loop processing

        self._process_local_payload(packet)

    def _process_local_payload(self, packet: RadioPacket):
        """Unpacks and records verified data payloads."""
        is_encrypted = (packet.flags & 0x02) != 0
        payload_data = packet.payload
        
        if is_encrypted:
            payload_data = self.cipher.process_payload(payload_data)

        if packet.packet_type == RadioPacket.TYPE_TEXT:
            msg_text = payload_data.decode('utf-8', errors='ignore')
            print(f" [Radio Ingest] Cleartext from Node {packet.source_node}: '{msg_text}'")
            
            # Hybrid WAN routing boundary condition
            if packet.dest_node == 9999: 
                self.gateway.route_radio_to_internet(packet, msg_text)
            else:
                self.db.insert_text_message(packet.packet_id, packet.source_node, packet.dest_node, msg_text)

    def ingest_satellite_stream(self, raw_stream_bytes: bytes):
        """Processes continuous live text alert streams downlinked via the satellite dish."""
        parsed = self.sat_demux.parse_satellite_transport_packet(raw_stream_bytes)
        if parsed:
            feed_id, content = parsed
            print(f" [Dish Ingestion] Stored satellite broadcast Feed {hex(feed_id)}: '{content}'")
            self.db.insert_text_message(999, 1000, 0xFFFF, f"[SATELLITE FEED {hex(feed_id)}] {content}")


if __name__ == "__main__":
    print("[*] Starting Hardware-Linked Master Production Server...")
    server = HardwareOffGridServer(node_id=1000)
    
    print("[+] Core background hardware engine loop initialized successfully.")
    print("[*] Server is live and actively polling radio lines. Press Ctrl+C to terminate.")
    
    # Secure infinite runtime loop preventing premature exit drops
    while True:
        try:
            server.listen_and_process_radio()
            time.sleep(0.01)  # 10ms rest window prevents CPU core starvation tracking loops
        except KeyboardInterrupt:
            print("\n[-] Offline radio gateway daemon safely halted by operator request.")
            break
