import time
import queue
from typing import Dict
from packet import RadioPacket
from services import SystemBeaconPayload

class VirtualRadioAirInterface:
    """
    Simulates physical RF radio wave propagation in software.
    """
    def __init__(self):
        self.active_nodes: Dict[int, queue.Queue] = {}

    def register_node(self, node_id: int) -> queue.Queue:
        node_queue = queue.Queue()
        self.active_nodes[node_id] = node_queue
        print(f"[Air Interface] Node {node_id} is online and listening to radio space.")
        return node_queue

    def broadcast_packet(self, sender_id: int, raw_frame: bytes):
        """Spreads the raw radio signal to all active listening nodes except the sender."""
        for target_id, rx_queue in self.active_nodes.items():
            if target_id != sender_id:
                rx_queue.put((sender_id, raw_frame))

class MockServerDaemon:
    """
    Simulates the core background broadcast tasks of the Raspberry Pi 4 Server.
    """
    def __init__(self, node_id: int, air_interface: VirtualRadioAirInterface):
        self.node_id: int = node_id
        self.air_interface: VirtualRadioAirInterface = air_interface
        self.rx_queue = self.air_interface.register_node(node_id)
        self.packet_counter: int = 0
        self.last_beacon_time: float = 0.0
        self.beacon_interval: float = 3.0

    def process_background_tasks(self):
        """Monitors clock thresholds to trigger automated beacons."""
        current_time = time.time()
        if current_time - self.last_beacon_time >= self.beacon_interval:
            self._transmit_discovery_beacon()
            self.last_beacon_time = current_time

    def _transmit_discovery_beacon(self):
        # 12-byte compiled telemetry payload matching services.py struct alignment
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
            dest_node=0xFFFF,  # Global broadcast
            packet_id=self.packet_counter,
            ttl=1,
            payload=beacon_data.serialize()
        )
        self.packet_counter = (self.packet_counter + 1) % 256
        print(f"\n [Server {self.node_id}] Pumping automatic discovery beacon into air waves...")
        self.air_interface.broadcast_packet(self.node_id, packet.serialize())

class MockESP32Handset:
    """
    Simulates a portable handset capturing server signals to populate the interface.
    """
    def __init__(self, node_id: int, air_interface: VirtualRadioAirInterface):
        self.node_id: int = node_id
        self.air_interface: VirtualRadioAirInterface = air_interface
        self.rx_queue = self.air_interface.register_node(node_id)

    def update(self):
        """Flushes the simulated hardware RX buffer FIFO queue."""
        while not self.rx_queue.empty():
            _, raw_bytes = self.rx_queue.get()
            packet = RadioPacket.deserialize(raw_bytes)
            if not packet:
                continue
            # Look for system control beacons matching our protocol design rules
            if packet.dest_node == 0xFFFF and packet.packet_type == RadioPacket.TYPE_ACK:
                print(f" [ESP32 Handset {self.node_id}] Found network! Click to select Server {packet.source_node}")

if __name__ == "__main__":
    print("[*] Starting Hardware-Free Radio Simulation environment...")
    air = VirtualRadioAirInterface()
    server = MockServerDaemon(node_id=1000, air_interface=air)
    handset = MockESP32Handset(node_id=201, air_interface=air)
    
    # Run a quick 2-tick loop step simulation to verify cross-module parsing link works
    for _ in range(2):
        server.process_background_tasks()
        handset.update()
        time.sleep(1)
