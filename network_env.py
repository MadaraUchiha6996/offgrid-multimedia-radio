import time
import queue

class VirtualRadioAirInterface:
    def __init__(self):
        self.active_nodes = {}

    def register_node(self, node_id):
        node_queue = queue.Queue()
        self.active_nodes[node_id] = node_queue
        print(f"Node {node_id} listening")
        return node_queue

    def broadcast_packet(self, sender_id, raw_frame):
        for target_id, rx_queue in self.active_nodes.items():
            if target_id != sender_id:
                rx_queue.put((sender_id, raw_frame))

class MockServerDaemon:
    def __init__(self, node_id, air_interface):
        self.node_id = node_id
        self.air_interface = air_interface
        self.rx_queue = self.air_interface.register_node(node_id)
        self.packet_counter = 0
        self.last_beacon_time = 0.0
        self.beacon_interval = 3.0

    def process_background_tasks(self):
        current_time = time.time()
        if current_time - self.last_beacon_time >= self.beacon_interval:
            self._transmit_discovery_beacon()
            self.last_beacon_time = current_time

    def _transmit_discovery_beacon(self):
        from services import SystemBeaconPayload
        from packet import RadioPacket
        
        beacon_data = SystemBeaconPayload(
            server_node_id=self.node_id,
            network_chan=4,
            flags=SystemBeaconPayload.FLAG_INTERNET_GATEWAY | SystemBeaconPayload.FLAG_SATELLITE_DISH,
            lat=28.6139,
            lon=77.2090
        )
        packet = RadioPacket(
            packet_type=RadioPacket.TYPE_ACK,
            source_node=self.node_id,
            dest_node=0xFFFF,  
            packet_id=self.packet_counter,
            ttl=1,
            payload=beacon_data.serialize()
        )
        self.packet_counter = (self.packet_counter + 1) % 256
        print(f"Server {self.node_id} sending discovery beacon")
        self.air_interface.broadcast_packet(self.node_id, packet.serialize())

class MockESP32Handset:
    def __init__(self, node_id, air_interface):
        self.node_id = node_id
        self.air_interface = air_interface
        self.rx_queue = self.air_interface.register_node(node_id)

    def update(self):
        from packet import RadioPacket
        while not self.rx_queue.empty():
            _, raw_bytes = self.rx_queue.get()
            packet = RadioPacket.deserialize(raw_bytes)
            if not packet:
                continue
            if packet.dest_node == 0xFFFF and packet.packet_type == RadioPacket.TYPE_ACK:
                print(f"Handset {self.node_id} found server {packet.source_node}")

if __name__ == "__main__":
    air = VirtualRadioAirInterface()
    server = MockServerDaemon(node_id=1000, air_interface=air)
    handset = MockESP32Handset(node_id=201, air_interface=air)
    
    for _ in range(2):
        server.process_background_tasks()
        handset.update()
        time.sleep(1)
