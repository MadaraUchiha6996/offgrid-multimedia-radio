import struct
from typing import Optional, Dict
from packet import RadioPacket

class SatelliteStreamDemux:
    """
    Parses and extracts structured data payloads received from a TV satellite dish 
    receiver link interface on the central Raspberry Pi 4 base station.
    
    Simulates demultiplexing a continuous broadcast feed into localized text bulletins.
    """
    def __init__(self):
        # Local table to cache parsed satellite alerts for handset query distribution
        self.downloaded_bulletins: Dict[int, str] = {}

    def parse_satellite_transport_packet(self, stream_bytes: bytes) -> Optional[tuple[int, str]]:
        """
        Parses a simulated DVB-S custom data frame downlinked from the dish antenna.
        
        Byte Structure:
        [2 Bytes: Feed Type ID] [1 Byte: Data Length] [Variable: Text Content]
        """
        if len(stream_bytes) < 3:
            return None
            
        try:
            feed_id, data_len = struct.unpack("<HB", stream_bytes[:3])
            content_bytes = stream_bytes[3:3 + data_len]
            content_text = content_bytes.decode('utf-8', errors='ignore')
            
            # Store parsed data in the server cache repository
            self.downloaded_bulletins[feed_id] = content_text
            return feed_id, content_text
        except struct.error:
            return None

    def package_for_mesh_request(self, feed_id: int, requestor_node: int, current_packet_id: int) -> Optional[RadioPacket]:
        """
        Extracts a cached satellite feed and packs it into a standard encrypted 
        RadioPacket structure ready to be pumped out to a requesting handset node.
        """
        if feed_id not in self.downloaded_bulletins:
            print(f"[-] Satellite Cache: Feed ID {feed_id} not available locally.")
            return None
            
        text_content = self.downloaded_bulletins[feed_id]
        raw_bytes = text_content.encode('utf-8')
        
        # Enforce strict 240 byte payload slicing check
        if len(raw_bytes) > 240:
            raw_bytes = raw_bytes[:240]  # Hard truncate to fit inside a single LoRa frame payload boundary

        return RadioPacket(
            packet_type=RadioPacket.TYPE_TEXT,
            source_node=1000,          # Server Node ID
            dest_node=requestor_node,  # Targeting the specific handset that asked for it
            packet_id=current_packet_id,
            ttl=4,                     # Standard mesh propagation limit
            flags=0x02,                # Enable the symmetric encryption flag bit
            payload=raw_bytes
        )


# --- Dedicated Validation Module Verification ---
if __name__ == "__main__":
    print("[*] Launching Satellite Dish Downlink Parser Validation...\n")
    demux = SatelliteStreamDemux()
    
    # 1. Generate a mock satellite stream packet downlinked through the dish tuner
    mock_feed_id = 0x88A1  # Example ID for Local Delhi Emergency Alert Bulletins
    mock_text = "ALERT: Water distribution center open at Sector 6. Supply status stable."
    mock_payload = mock_text.encode('utf-8')
    
    header = struct.pack("<HB", mock_feed_id, len(mock_payload))
    simulated_satellite_stream = header + mock_payload
    
    # 2. Run parsing demux test
    print("[*] Processing raw incoming satellite stream block...")
    result = demux.parse_satellite_transport_packet(simulated_satellite_stream)
    
    assert result is not None, "Failed to parse satellite stream format."
    print(f"[+] Success! Parsed Satellite Feed {hex(result[0])}: '{result[1]}'")
    
    # 3. Simulate an offline ESP32 node pulling this news block from the server cache
    print("\n[*] Packaging parsed satellite content into an off-grid network packet...")
    outbound_packet = demux.package_for_mesh_request(feed_id=0x88A1, requestor_node=201, current_packet_id=44)
    
    assert outbound_packet is not None
    assert outbound_packet.dest_node == 201
    print(f"[+] RadioPacket generated cleanly. Frame Size: {len(outbound_packet.serialize())} bytes.")
    print(f"    Ready to route to Handset 201 across the ad-hoc mesh channels.")

