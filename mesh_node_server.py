import time
from typing import Dict, List, Tuple, Optional
from packet import RadioPacket
from services import GPSPayload, SystemBeaconPayload
from routing import MeshRouter
from security import OffGridCipher

class ESP32NodeServer:
    """
    Simulates the firmware running on an ESP32-S3 node acting as a small server.
    Implements auto-connect beacon processing, localized data store-and-forward, 
    GPS tracking telemetry, and message historical request pull queues.
    """
    def __init__(self, node_id: int, air_interface):
        self.node_id: int = node_id
        self.air = air_interface
        self.rx_queue = self.air.register_node(node_id)
        
        # Sub-system allocations
        self.router = MeshRouter(node_id=node_id)
        self.cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
        
        # Micro-server Local Storage Banks
        self.local_inbox: List[Dict[str, any]] = []      # Stored messages for THIS specific node
        self.transit_buffer: List[RadioPacket] = []     # Store-and-forward pool for other offline nodes
        
        # Operational States
        self.connected_gateway_id: Optional[int] = None
        self.packet_counter: int = 0
        self.latitude: float = 28.6139  # Baseline Delhi coordinates
        self.longitude: float = 77.2090

    def update_gps(self, lat: float, lon: float):
        """Simulates internal hardware GPS updating its tracking location coordinates."""
        self.latitude = lat
        self.longitude = lon

    def send_broadcast_text(self, text: str):
        """Encrypts and broadcasts a message across the mesh topology."""
        raw_payload = text.encode('utf-8')
        encrypted_payload = self.cipher.process_payload(raw_payload)
        
        packet = RadioPacket(
            packet_type=RadioPacket.TYPE_TEXT,
            source_node=self.node_id,
            dest_node=0xFFFF,  # Broadcast destination
            packet_id=self.packet_counter,
            ttl=4,
            flags=0x02,  # Encryption set bit
            payload=encrypted_payload
        )
        self.packet_counter = (self.packet_counter + 1) % 256
        print(f"🚀 [ESP32 Node {self.node_id}] Spreading network text signal block...")
        self.air.broadcast_packet(self.node_id, packet.serialize())

    def request_old_messages(self, target_server_id: int):
        """Pumps a specific REQ_MSG frame to pull historical logs from a target server node."""
        packet = RadioPacket(
            packet_type=RadioPacket.TYPE_REQ_MSG,
            source_node=self.node_id,
            dest_node=target_server_id,
            packet_id=self.packet_counter,
            ttl=4,
            flags=0x00,
            payload=b""  # Header alone signals the demand request parameters
        )
        self.packet_counter = (self.packet_counter + 1) % 256
        print(f"📥 [ESP32 Node {self.node_id}] Querying Node {target_server_id} for historical pending inbox queue records...")
        self.air.broadcast_packet(self.node_id, packet.serialize())

    def process_radio_cycle(self):
        """Main non-blocking execution loop processing the mesh operations."""
        while not self.rx_queue.empty():
            sender_id, raw_bytes = self.rx_queue.get()
            packet = RadioPacket.deserialize(raw_bytes)
            if not packet:
                continue

            # Run through mesh routing filters
            action, forward_list = self.router.process_incoming_frame(packet)
            
            if action == "DROP_DUPLICATE":
                continue

            # Spreading the code: handle transit packets to forward immediately
            for pkt in forward_list:
                print(f"🔁 [ESP32 Node {self.node_id}] Re-broadcasting/Spreading transit packet from Node {pkt.source_node}")
                self.air.broadcast_packet(self.node_id, pkt.serialize())

            if action in ["CONSUME_LOCAL", "CONSUME_AND_FORWARD"]:
                self._execute_local_server_logic(packet)

    def _execute_local_server_logic(self, packet: RadioPacket):
        """The core miniature server operational protocol execution engine."""
        
        # Feature 1: Auto Connect Code Processing via Beacon Monitoring
        if packet.packet_type == RadioPacket.TYPE_ACK and packet.dest_node == 0xFFFF:
            beacon = SystemBeaconPayload.deserialize(packet.payload)
            if beacon and self.connected_gateway_id != packet.source_node:
                self.connected_gateway_id = packet.source_node
                print(f"⚡ [ESP32 Node {self.node_id}] AUTO-CONNECT SUCCESS: Linked to central base anchor Node {self.connected_gateway_id}")

        # Feature 2: Historical Request Pull Verification Handler (REQ_MSG)
        elif packet.packet_type == RadioPacket.TYPE_REQ_MSG:
            print(f"🕵️ [ESP32 Mini-Server {self.node_id}] Received data query fetch command from Node {packet.source_node}")
            self._flush_stored_transit_packets_for_node(packet.source_node)

        # Feature 3: Secured Message Storage Consume Handler
        elif packet.packet_type == RadioPacket.TYPE_TEXT:
            is_encrypted = (packet.flags & 0x02) != 0
            payload = self.cipher.process_payload(packet.payload) if is_encrypted else packet.payload
            decoded_text = payload.decode('utf-8', errors='ignore')
            
            self.local_inbox.append({"src": packet.source_node, "text": decoded_text, "time": time.time()})
            print(f"📥 [ESP32 Node {self.node_id} Inbox] Message Received: '{decoded_text}' from Node {packet.source_node}")

    def _flush_stored_transit_packets_for_node(self, target_node: int):
        """Flushes matching cached frames down the network pipeline to the requesting node."""
        # Check transit buffer if this small server cached data for them while they were offline
        matching_frames = [p for p in self.transit_buffer if p.dest_node == target_node]
        if not matching_frames:
            print(f"└─ [Result] No historical logs queued for Node {target_node} at this sector.")
            return

        for pkt in matching_frames:
            self.air.broadcast_packet(self.node_id, pkt.serialize())
            self.transit_buffer.remove(pkt)
        print(f"└─ [Success] Dispatched and flushed structural history frames down to Node {target_node}.")


# --- Complete Architecture Simulation Loop ---
if __name__ == "__main__":
    print("[*] Launching Complete Decoupled Small-Server Mesh Infrastructure...\n")
    from network_env import VirtualRadioAirInterface
    
    air = VirtualRadioAirInterface()
    
    # Instantiate 3 localized ESP32 node servers interacting peer-to-peer
    node_A = ESP32NodeServer(node_id=201, air_interface=air)
    node_B = ESP32NodeServer(node_id=202, air_interface=air)  # Mid-hop node
    node_C = ESP32NodeServer(node_id=203, air_interface=air)  # Distant server cache node
    
    # 1. Simulate a master anchor configuration presence beacon injection
    from services import SystemBeaconPayload
    mock_beacon_payload = SystemBeaconPayload(server_node_id=1000, network_chan=4, flags=1, lat=28.6, lon=77.2).serialize()
    beacon_packet = RadioPacket(packet_type=RadioPacket.TYPE_ACK, source_node=1000, dest_node=0xFFFF, packet_id=1, ttl=1, payload=mock_beacon_payload)
    
    print("--- Phase 1: Automated Broadcast Detection & Tracking ---")
    air.broadcast_packet(sender_id=1000, raw_frame=beacon_packet.serialize())
    node_A.process_radio_cycle()
    node_B.process_radio_cycle()
    
    print("\n--- Phase 2: Mesh Propagation & Signal Spreading ---")
    node_A.send_broadcast_text("Alert: Grid Offline, switching to local store-and-forward loops.")
    node_B.process_radio_cycle()  # Catches, registers, and automatically spreads it forward
    node_C.process_radio_cycle()  # Catches the propagated frame from Node B cleanly
    
    print("\n--- Phase 3: Historical Data Query Requests ---")
    # Cache a message into Node C's mini-server transit buffer bound for Node A
    clandestine_msg = RadioPacket(packet_type=RadioPacket.TYPE_TEXT, source_node=203, dest_node=201, packet_id=88, ttl=4, payload=node_C.cipher.process_payload("Secret update cache block.".encode('utf-8')))
    node_C.transit_buffer.append(clandestine_msg)
    
    # Node A calls a remote history log sync request directly targeting Node C
    node_A.request_old_messages(target_server_id=203)
    node_B.process_radio_cycle()  # Passes request forward
    node_C.process_radio_cycle()  # Node C swallows it, evaluates its local database cache, and flushes bytes back
