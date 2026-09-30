import time
from packet import RadioPacket
from services import GPSPayload, SystemBeaconPayload
from routing import MeshRouter
from security import OffGridCipher

class ESP32NodeServer:
    def __init__(self, node_id, air_interface):
        self.node_id = node_id
        self.air = air_interface
        self.rx_queue = self.air.register_node(node_id)
        
        self.router = MeshRouter(node_id=node_id)
        self.cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
        
        self.local_inbox = []      
        self.transit_buffer = []     
        
        self.connected_gateway_id = None
        self.packet_counter = 0
        self.latitude = 28.6139  
        self.longitude = 77.2090

    def update_gps(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def send_broadcast_text(self, text):
        raw_payload = text.encode('utf-8')
        encrypted_payload = self.cipher.process_payload(raw_payload)
        
        packet = RadioPacket(
            packet_type=RadioPacket.TYPE_TEXT,
            source_node=self.node_id,
            dest_node=0xFFFF,  
            packet_id=self.packet_counter,
            ttl=4,
            flags=0x02,  
            payload=encrypted_payload
        )
        self.packet_counter = (self.packet_counter + 1) % 256
        print(f"Sending broadcast from node {self.node_id}")
        self.air.broadcast_packet(self.node_id, packet.serialize())

    def request_old_messages(self, target_server_id: int):
        packet = RadioPacket(
            packet_type=RadioPacket.TYPE_REQ_MSG,
            source_node=self.node_id,
            dest_node=target_server_id,
            packet_id=self.packet_counter,
            ttl=4,
            flags=0x00,
            payload=b""  
        )
        self.packet_counter = (self.packet_counter + 1) % 256
        print(f"Requesting history logs from node {target_server_id}")
        self.air.broadcast_packet(self.node_id, packet.serialize())

    def process_radio_cycle(self):
        while not self.rx_queue.empty():
            sender_id, raw_bytes = self.rx_queue.get()
            packet = RadioPacket.deserialize(raw_bytes)
            if not packet:
                continue

            action, forward_list = self.router.process_incoming_frame(packet)
            if action == "DROP_DUPLICATE":
                continue

            for pkt in forward_list:
                print(f"Forwarding packet from node {pkt.source_node}")
                self.air.broadcast_packet(self.node_id, pkt.serialize())

            if action in ["CONSUME_LOCAL", "CONSUME_AND_FORWARD"]:
                self._execute_local_server_logic(packet)

    def _execute_local_server_logic(self, packet):
        if packet.packet_type == RadioPacket.TYPE_ACK and packet.dest_node == 0xFFFF:
            beacon = SystemBeaconPayload.deserialize(packet.payload)
            if beacon and self.connected_gateway_id != packet.source_node:
                self.connected_gateway_id = packet.source_node
                print(f"Connected to base node {self.connected_gateway_id}")

        elif packet.packet_type == RadioPacket.TYPE_REQ_MSG:
            print(f"Handling data fetch command from node {packet.source_node}")
            self._flush_stored_transit_packets_for_node(packet.source_node)

        elif packet.packet_type == RadioPacket.TYPE_TEXT:
            is_encrypted = (packet.flags & 0x02) != 0
            payload = self.cipher.process_payload(packet.payload) if is_encrypted else packet.payload
            decoded_text = payload.decode('utf-8', errors='ignore')
            
            self.local_inbox.append({"src": packet.source_node, "text": decoded_text, "time": time.time()})
            print(f"Received message from node {packet.source_node}")

    def _flush_stored_transit_packets_for_node(self, target_node):
        matching_frames = [p for p in self.transit_buffer if p.dest_node == target_node]
        if not matching_frames:
            return

        for pkt in matching_frames:
            self.air.broadcast_packet(self.node_id, pkt.serialize())
            self.transit_buffer.remove(pkt)
        print(f"Flushed history logs to node {target_node}")

if __name__ == "__main__":
    from network_env import VirtualRadioAirInterface
    
    air = VirtualRadioAirInterface()
    node_A = ESP32NodeServer(node_id=201, air_interface=air)
    node_B = ESP32NodeServer(node_id=202, air_interface=air)  
    node_C = ESP32NodeServer(node_id=203, air_interface=air)  
    
    from services import SystemBeaconPayload
    mock_beacon_payload = SystemBeaconPayload(server_node_id=1000, network_chan=4, flags=1, lat=28.6, lon=77.2).serialize()
    beacon_packet = RadioPacket(packet_type=RadioPacket.TYPE_ACK, source_node=1000, dest_node=0xFFFF, packet_id=1, ttl=1, payload=mock_beacon_payload)
    
    print("Testing tracking...")
    air.broadcast_packet(sender_id=1000, raw_frame=beacon_packet.serialize())
    node_A.process_radio_cycle()
    node_B.process_radio_cycle()
    
    print("Testing propagation...")
    node_A.send_broadcast_text("Alert: Grid Offline")
    node_B.process_radio_cycle()  
    node_C.process_radio_cycle()  
