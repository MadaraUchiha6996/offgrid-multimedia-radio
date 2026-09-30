import time


class MeshNetworkRouter:

    def __init__(self):
        self.hi, self.std = [], []  # Native lists eliminate deque overhead

    def ingress_packet(self, raw, rssi, snr):
        pkt = {"payload": raw, "rssi": rssi, "snr": snr, "arrival_time": time.time()}
        # Minimalist priority grouping
        (self.hi if any(a in raw for a in ("I NEED HELP", "RESCUE ME")) else self.std).append(pkt)

    def process_next_packet(self):
        # Native array truthiness checks prioritize high-priority packets first
        return self.hi.pop(0) if self.hi else (self.std.pop(0) if self.std else None)

    def calculate_mesh_health(self, tracked_nodes):
        t = time.time()
        # Clean dictionary comprehension handles the loop natively
        return {
            n_id: {
                "name": d.get("friendly_name", f"Node #{n_id}"),
                "status": "STABLE" if t - d.get("last_seen_epoch", t) <= 45 else "DEGRADED / STALLED",
                "link_margin_rssi": d.get("last_rssi", -120.0),
            }
            for n_id, d in tracked_nodes.items()
        }


if __name__ == "__main__":
    router = MeshNetworkRouter()
    router.ingress_packet("[SRC:126][DST:SERVER] Moving down ridge line...", -72.0, 8.0)
    router.ingress_packet("[SRC:996][DST:SERVER] I NEED HELP", -94.0, 3.2)
    next_up = router.process_next_packet()
