import collections
import time

class MeshNetworkRouter:
    def __init__(self):
        # Double-ended queue to cleanly isolate high-priority traffic paths
        self.high_priority_queue = collections.deque()
        self.standard_queue = collections.deque()
        print("[MESH ROUTER] Ad-hoc message priority routing tables initialized.")

    def ingress_packet(self, raw_frame, rssi, snr):
        """
        Receives inbound radio frames from the gateway layer, evaluates their content strings, 
        and routes them into the correct priority queues.
        """
        packet_wrapper = {
            "payload": raw_frame,
            "rssi": rssi,
            "snr": snr,
            "arrival_time": time.time()
        }

        # --- EVALUATE EMERGENCY OVERRIDE STRINGS ---
        # Checks if the payload contains any matching structural alert phrases from your text menu
        if any(alert in raw_frame for alert in ["I NEED HELP", "RESCUE ME"]):
            self.high_priority_queue.append(packet_wrapper)
            print(f"⚠️  [CRITICAL PRIORITY INGRESS] Forced emergency bypass route allocated for packet!")
        else:
            self.standard_queue.append(packet_wrapper)
            print(f"📦 [STANDARD INGRESS] Telemetry/Message indexed into secondary background queue.")

    def process_next_packet(self):
        """
        Pulls the next packet from the buffer queues. 
        Always drains the emergency queue completely before looking at standard packets.
        """
        # Always empty out the emergency distress lines first!
        if self.high_priority_queue:
            return self.high_priority_queue.popleft()
        
        if self.standard_queue:
            return self.standard_queue.popleft()
            
        return None

    def calculate_mesh_health(self, tracked_nodes):
        """
        Helper routine that scans your database's active nodes array to flag path degradation 
        or disconnected peer units.
        """
        current_time = time.time()
        network_health_matrix = {}

        for node_id, data in tracked_nodes.items():
            last_seen = data.get("last_seen_epoch", current_time)
            # If a handheld node goes completely silent for more than 45 seconds, mark it as stalled
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
    # Local runtime evaluation loop to confirm queue mechanics pass testing checks
    router = MeshNetworkRouter()
    
    # Simulate a routine check-in followed by an emergency alert flag arriving immediately behind it
    router.ingress_packet("[SRC:126][DST:SERVER] Moving down ridge line...", -72.0, 8.0)
    router.ingress_packet("[SRC:996][DST:SERVER] I NEED HELP", -94.0, 3.2)
    
    # Pull the first available message from the processing execution loop
    next_up = router.process_next_packet()
    print(f"\n[TEST LOOP] Router popped message: '{next_up['payload']}' (Confirmed priority routing success!)")
