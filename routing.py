import collections
import time

class MeshNetworkRouter:
    def __init__(self):
        self.high_priority_queue = collections.deque()
        self.standard_queue = collections.deque()

    def ingress_packet(self, raw_frame, rssi, snr):
        packet_wrapper = {
            "payload": raw_frame,
            "rssi": rssi,
            "snr": snr,
            "arrival_time": time.time()
        }

        if any(alert in raw_frame for alert in ["I NEED HELP", "RESCUE ME"]):
            self.high_priority_queue.append(packet_wrapper)
        else:
            self.standard_queue.append(packet_wrapper)

    def process_next_packet(self):
        if self.high_priority_queue:
            return self.high_priority_queue.popleft()
        
        if self.standard_queue:
            return self.standard_queue.popleft()
            
        return None

    def calculate_mesh_health(self, tracked_nodes):
        current_time = time.time()
        network_health_matrix = {}

        for node_id, data in tracked_nodes.items():
            last_seen = data.get("last_seen_epoch", current_time)
            if current_time - last_seen > 45:
                status = "DEGRADED / STALLED"
            else:
                status = "STABLE"
                
            network_health_matrix[node_id] = {
                "name": data.get("friendly_name", f"Node #{node_id}"),
                "status": status,
                "link_margin_rssi": data.get("last_rssi", -120.0)
            }
        return network_health_matrix

if __name__ == "__main__":
    router = MeshNetworkRouter()
    router.ingress_packet("[SRC:126][DST:SERVER] Moving down ridge line...", -72.0, 8.0)
    router.ingress_packet("[SRC:996][DST:SERVER] I NEED HELP", -94.0, 3.2)
    next_up = router.process_next_packet()
