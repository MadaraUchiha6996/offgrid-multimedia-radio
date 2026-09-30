import time
from packet import RadioPacket
from routing import MeshRouter
from security import OffGridCipher
from services import SystemBeaconPayload


class ESP32NodeServer:

    def __init__(self, node_id, air_interface):
        self.node_id = node_id
        self.air = air_interface
        self.rx_queue = self.air.register_node(node_id)
        self.router = MeshRouter(node_id=node_id)
        self.cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")

        self.local_inbox, self.transit_buffer = [], []
        self.connected_gateway_id = None
        self.packet_counter = 0
        self.latitude, self.longitude = 28.6139, 77.2090

    def update_gps(self, lat, lon):
        self.latitude, self.longitude = lat, lon

    def _send_pkt(self, p_type, dest, flags, payload, msg=""):
        # Centralized packet factory builder to eliminate structural bloat
        pkt = RadioPacket(
            packet_type=p_type,
            source_node=self.node_id,
            dest_node=dest,
            packet_id=self.packet_counter,
            ttl=4,
            flags=flags,
            payload=payload,
        )
        self.packet_counter = (self.packet_counter + 1) & 0xFF  # Native fast bitmask
        if msg:
            print(msg)
        self.air.broadcast_packet(self.node_id, pkt.serialize())

    def send_broadcast_text(self, text):
        self._send_pkt(
            RadioPacket.TYPE_TEXT,
            0xFFFF,
            0x02,
            self.cipher.process_payload(text.encode("utf-8")),
            f"Sending broadcast from node {self.node_id}",
        )

    def request_old_messages(self, target_server_id: int):
        self._send_pkt(
            RadioPacket.TYPE_REQ_MSG,
            target_server_id,
            0x00,
            b"",
            f"Requesting history logs from node {target_server_id}",
        )

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

            if action in ("CONSUME_LOCAL", "CONSUME_AND_FORWARD"):
                self._execute_local_server_logic(packet)

    def _execute_local_server_logic(self, packet):
        if packet.packet_type == RadioPacket.TYPE_ACK and packet.dest_node == 0xFFFF:
            b = SystemBeaconPayload.deserialize(packet.payload)
            if b and self.connected_gateway_id != packet.source_node:
                self.connected_gateway_id = packet.source_node
                print(f"Connected to base node {self.connected_gateway_id}")

        elif packet.packet_type == RadioPacket.TYPE_REQ_MSG:
            print(f"Handling data fetch command from node {packet.source_node}")
            self._flush_stored_transit_packets_for_node(packet.source_node)

        elif packet.packet_type == RadioPacket.TYPE_TEXT:
            p = (
                self.cipher.process_payload(packet.payload)
                if (packet.flags & 0x02)
                else packet.payload
            )
            self.local_inbox.append(
                {
                    "src": packet.source_node,
                    "text": p.decode("utf-8", errors="ignore"),
                    "time": time.time(),
                }
            )
            print(f"Received message from node {packet.source_node}")

    def _flush_stored_transit_packets_for_node(self, target_node):
        # Native safe split execution without altering items inside the processing loop
        to_send = [p for p in self.transit_buffer if p.dest_node == target_node]
        self.transit_buffer = [p for p in self.transit_buffer if p.dest_node != target_node]

        for pkt in to_send:
            self.air.broadcast_packet(self.node_id, pkt.serialize())
        if to_send:
            print(f"Flushed history logs to node {target_node}")


if __name__ == "__main__":
    from network_env import VirtualRadioAirInterface

    air = VirtualRadioAirInterface()
    node_A = ESP32NodeServer(201, air)
    node_B = ESP32NodeServer(202, air)
    node_C = ESP32NodeServer(203, air)

    m_payload = SystemBeaconPayload(1000, 4, 1, 28.6, 77.2).serialize()
    b_pkt = RadioPacket(RadioPacket.TYPE_ACK, 1000, 0xFFFF, 1, 1, payload=m_payload)

    print("Testing tracking...")
    air.broadcast_packet(1000, b_pkt.serialize())
    node_A.process_radio_cycle()
    node_B.process_radio_cycle()

    print("Testing propagation...")
    node_A.send_broadcast_text("Alert: Grid Offline")
    node_B.process_radio_cycle()
    node_C.process_radio_cycle()
