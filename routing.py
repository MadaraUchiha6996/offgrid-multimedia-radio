import time
from typing import Dict, List, Tuple
from packet import RadioPacket

class MeshRouter:
    """
    Manages custom ad-hoc mesh routing tables, packet forwarding logic,
    and duplicate frame filtering for the off-grid radio network.
    """
    def __init__(self, node_id: int):
        self.node_id: int = node_id
        # Tracks recently seen packets to prevent infinite looping echoes: (source_node, packet_id) -> timestamp
        self.seen_packets: Dict[Tuple[int, int], float] = {}
        # Simple routing table map: destination_node -> next_hop_node
        self.routing_table: Dict[int, int] = {}
        # Retention window to clear out dead deduplication records (in seconds)
        self.dedup_timeout: float = 30.0

    def should_process_packet(self, packet: RadioPacket) -> bool:
        """
        Applies strict filtering logic to drop duplicate frames 
        and clear out old tracking entries.
        """
        current_time = time.time()
        
        # Housekeeping: Purge stale tracking logs to optimize memory tracking footprint
        stale_keys = [k for k, v in self.seen_packets.items() if current_time - v > self.dedup_timeout]
        for k in stale_keys:
            del self.seen_packets[k]

        # Deduplication check
        packet_key = (packet.source_node, packet.packet_id)
        if packet_key in self.seen_packets:
            return False  # We have already seen/forwarded this exact packet. Drop it.

        # Log this brand new packet signature immediately
        self.seen_packets[packet_key] = current_time
        return True

    def process_incoming_frame(self, packet: RadioPacket) -> Tuple[str, List[RadioPacket]]:
        """
        Analyzes the routing headers to determine if the payload is bound for 
        the local node, needs global broadcasting, or requires hopping forward.
        
        Returns:
            Tuple[action_type, list_of_packets_to_send]
        """
        # Step 1: Check deduplication safety guard rails
        if not self.should_process_packet(packet):
            return "DROP_DUPLICATE", []

        # Step 2: Check if the packet is meant specifically for us or a global broadcast
        if packet.dest_node == self.node_id:
            return "CONSUME_LOCAL", []
        
        if packet.dest_node == 0xFFFF:
            # Broadcast frames are consumed locally AND forwarded down the line if TTL permits
            forwarded_packets = []
            if packet.ttl > 1:
                packet.ttl -= 1  # Degrade life threshold counter
                forwarded_packets.append(packet)
            return "CONSUME_AND_FORWARD", forwarded_packets

        # Step 3: Handle structural message transit forwarding (Unicast routing)
        if packet.ttl <= 1:
            print(f"[-] Node {self.node_id}: Packet TTL expired. Dropping frame.")
            return "DROP_TTL_EXPIRED", []

        # Degrade hop threshold limit before sending down the mesh pipeline
        packet.ttl -= 1
        print(f"🔗 [Mesh Node {self.node_id}] Routing frame forward: Src {packet.source_node} -> Dst {packet.dest_node} (New TTL: {packet.ttl})")
        return "FORWARD", [packet]

    def update_route(self, destination: int, next_hop: int):
        """Manually links or updates an efficient path vector across nodes."""
        self.routing_table[destination] = next_hop


# --- Structural Unit Sanity Validation ---
if __name__ == "__main__":
    print("[*] Verifying mesh routing layer logic thresholds...")
    router = MeshRouter(node_id=202)  # Middle hop node setup
    
    test_packet = RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=101,
        dest_node=303,  # Target is beyond us
        packet_id=7,
        ttl=4
    )
    
    # Check 1: Verify forwarding path behavior
    action, forward_list = router.process_incoming_frame(test_packet)
    assert action == "FORWARD", "Routing layer failed to detect transit hop target."
    assert forward_list[0].ttl == 3, "TTL degradation tracking logic failed deduction test."
    
    # Check 2: Verify duplicate tracking block safety limits
    second_action, _ = router.process_incoming_frame(test_packet)
    assert second_action == "DROP_DUPLICATE", "Deduplication storm safety failure detected."
    
    print("[+] All custom mesh routing integrity verifications PASSED cleanly.")
