import time
import os
import struct
from packet import RadioPacket
from services import SystemBeaconPayload
from network_env import VirtualRadioAirInterface
from routing import MeshRouter
from audio_codec import AudioStreamChunk, AudioReassembler
from database import OffGridDatabase
from security import OffGridCipher
from gateway import OffGridInternetGateway
from satellite_receiver import SatelliteStreamDemux

class MasterOffGridServer:
    """
    The master server engine running on the central Raspberry Pi 4.
    Orchestrates routing, decryption, voice reassembly, database engine tasks,
    internet bridging, and live TV satellite dish broadcast stream ingestion.
    """
    def __init__(self, node_id: int, air_interface: VirtualRadioAirInterface):
        self.node_id = node_id
        self.air = air_interface
        self.rx_queue = self.air.register_node(node_id)
        
        # Initialize core sub-systems
        self.router = MeshRouter(node_id=node_id)
        self.assembler = AudioReassembler()
        self.db = OffGridDatabase("live_radio_records.db")
        self.cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
        self.gateway = OffGridInternetGateway()
        self.sat_demux = SatelliteStreamDemux()
        
        self.packet_counter = 0
        print(f"[Master Server] Node {self.node_id} fully compiled. WAN Gateway & DVB-S Satellite Ingestion active.")

    def ingest_satellite_stream(self, raw_stream_bytes: bytes):
        """
        Simulates receiving a high-frequency telemetry burst from the TV dish receiver card.
        Parses it and stores it in the central emergency database repository.
        """
        parsed = self.sat_demux.parse_satellite_transport_packet(raw_stream_bytes)
        if parsed:
            feed_id, content = parsed
            print(f" [Dish Ingestion] Successfully extracted satellite broadcast Feed {hex(feed_id)}: '{content}'")
            # Commit it safely to database records for offline handset query mapping
            self.db.insert_text_message(
                packet_id=999, 
                src=1000, 
                dest=0xFFFF, 
                text=f"[SATELLITE FEED {hex(feed_id)}] {content}"
            )

    def update(self):
        """Flushes the radio line buffers and acts on arriving signals."""
        while not self.rx_queue.empty():
            sender_id, raw_bytes = self.rx_queue.get()
            packet = RadioPacket.deserialize(raw_bytes)
            if not packet:
                continue

            # Run through mesh routing checks
            action, forward_list = self.router.process_incoming_frame(packet)
            
            if action == "DROP_DUPLICATE":
                continue
                
            if action in ["CONSUME_LOCAL", "CONSUME_AND_FORWARD"]:
                self._handle_local_payload(packet)
                
            # If the mesh routing logic flagged it to pass forward, re-broadcast it
            for pkt_to_forward in forward_list:
                self.air.broadcast_packet(self.node_id, pkt_to_forward.serialize())

    def _handle_local_payload(self, packet: RadioPacket):
        """Unpacks and processes data meant specifically for the server or external gateway."""
        is_encrypted = (packet.flags & 0x02) != 0
        payload_data = packet.payload
        
        if is_encrypted:
            payload_data = self.cipher.process_payload(payload_data)

        if packet.packet_type == RadioPacket.TYPE_TEXT:
            msg_text = payload_data.decode('utf-8', errors='ignore')
            print(f"[Server Store] Received Cleartext from Node {packet.source_node}: '{msg_text}'")
            
            # Smart Gateway Routing: If the packet is explicitly meant for an outside link, push to WAN
            if packet.dest_node == 9999: 
                self.gateway.route_radio_to_internet(packet, msg_text)
            else:
                self.db.insert_text_message(packet.packet_id, packet.source_node, packet.dest_node, msg_text)

        elif packet.packet_type == RadioPacket.TYPE_VOICE:
            voice_chunk = AudioStreamChunk.deserialize(payload_data)
            if not voice_chunk:
                return
                
            print(f" [Server Audio] Processing segment {voice_chunk.chunk_index + 1}/{voice_chunk.total_chunks} from Node {packet.source_node}")
            complete, full_voice_note = self.assembler.add_chunk(voice_chunk)
            
            if complete and full_voice_note:
                file_name = f"voice_msg_{voice_chunk.message_id}.bin"
                with open(file_name, "wb") as f:
                    f.write(full_voice_note)
                    
                print(f" [SUCCESS] Voice Note {voice_chunk.message_id} fully assembled and saved to: {file_name}")
                self.db.insert_voice_record(voice_chunk.message_id, packet.source_node, file_name)


# --- Full Integration Test Loop ---
if __name__ == "__main__":
    print("[*] Launching Master Off-Grid Integrated System Test...\n")
    air_space = VirtualRadioAirInterface()
    server = MasterOffGridServer(node_id=1000, air_interface=air_space)
    
    print("\n--- Step 1: Simulating Dish Inbound Satellite Feed Ingestion ---")
    mock_feed_id = 0x88A1
    mock_text = "CRITICAL: Clean drinking water distribution site set up at Sector 6 grid."
    mock_payload = mock_text.encode('utf-8')
    simulated_stream = struct.pack("<HB", mock_feed_id, len(mock_payload)) + mock_payload
    
    # Push the satellite data straight into our running server coordinator engine
    server.ingest_satellite_stream(simulated_stream)
    
    print("\n--- Step 2: Simulating Handset Text to Internet Gateway Routing ---")
    handset_cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
    gateway_msg = "SOS: Handset 201 coordinates tracking safe. Requesting external emergency services relay."
    
    gateway_packet = RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=201,
        dest_node=9999,  # Reserved virtual destination ID for direct outward internet routing
        packet_id=55,
        ttl=3,
        flags=0x02,  # Encrypted frame indicator
        payload=handset_cipher.process_payload(gateway_msg.encode('utf-8'))
    )
    
    # Broadcast to the air waves
    air_space.broadcast_packet(sender_id=201, raw_frame=gateway_packet.serialize())
    
    # Update server loop to parse the air waves traffic
    server.update()
    
    print("\n[+] Integrated master script tracking cycle completed cleanly.")
