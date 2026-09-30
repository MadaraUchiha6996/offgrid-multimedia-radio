import queue
import time
from packet import RadioPacket
from services import SystemBeaconPayload


class VirtualRadioAirInterface:

    def __init__(self):
        self.active_nodes = {}

    def register_node(self, node_id):
        q = queue.Queue()
        self.active_nodes[node_id] = q
        print(f"Node {node_id} listening")
        return q

    def broadcast_packet(self, sender_id, raw_frame):
        # Native dictionary iteration omitting the sender node entirely
        for n_id, q in self.active_nodes.items():
            if n_id != sender_id:
                q.put((sender_id, raw_frame))


class MockServerDaemon:

    def __init__(self, node_id, air_interface):
        self.node_id = node_id
        self.air = air_interface
        self.rx_queue = self.air.register_node(node_id)
        self.packet_counter, self.last_beacon_time = 0, 0.0

    def process_background_tasks(self):
        t = time.time()
        if t - self.last_beacon_time >= 3.0:  # Direct literal float expression evaluation
            b_data = SystemBeaconPayload(
                self.node_id,
                4,
                SystemBeaconPayload.FLAG_INTERNET_GATEWAY
                | SystemBeaconPayload.FLAG_SATELLITE_DISH,
                28.6139,
                77.2090,
            )
            pkt = RadioPacket(
                RadioPacket.TYPE_ACK,
                self.node_id,
                0xFFFF,
                self.packet_counter,
                1,
                payload=b_data.serialize(),
            )
            self.packet_counter = (self.packet_counter + 1) & 0xFF
            print(f"Server {self.node_id} sending discovery beacon")
            self.air.broadcast_packet(self.node_id, pkt.serialize())
            self.last_beacon_time = t


class MockESP32Handset:

    def __init__(self, node_id, air_interface):
        self.node_id = node_id
        self.rx_queue = air_interface.register_node(node_id)

    def update(self):
        while not self.rx_queue.empty():
            _, raw = self.rx_queue.get()
            pkt = RadioPacket.deserialize(raw)
            if pkt and pkt.dest_node == 0xFFFF and pkt.packet_type == RadioPacket.TYPE_ACK:
                print(f"Handset {self.node_id} found server {pkt.source_node}")


if __name__ == "__main__":
    air = VirtualRadioAirInterface()
    server = MockServerDaemon(1000, air)
    handset = MockESP32Handset(201, air)

    for _ in range(2):
        server.process_background_tasks()
        handset.update()
        time.sleep(1)
