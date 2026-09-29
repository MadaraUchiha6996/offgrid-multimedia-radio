import struct

# --- AD-HOC PACKET TYPE IDENTIFIERS ---
PACKET_TYPE_HANDSHAKE = 0x01  # Matches handheld's [SYS_INIT] boot check-in
PACKET_TYPE_TEXT      = 0x02  # Standard text strings
PACKET_TYPE_VOICE     = 0x03  # Handheld voice notes data chunk marker

class OffGridPacketEngine:
    def __init__(self):
        # Master header format signature matching standard microcontroller structures
        # 1 Byte Source ID, 1 Byte Target ID, 1 Byte Type Flag, 1 Byte Data Length Code
        self.header_format = ">BBBB" 
        print("[PACKET ENGINE] Binary air serialization framework initialized.")

    def serialize_text_packet(self, source_id, target_id, message_str):
        """
        Takes human-readable text inputs and bundles them into an efficient 
        binary string sequence optimized for sub-GHz radio transmission lanes.
        """
        payload_bytes = message_str.encode('utf-8')
        length = len(payload_bytes)
        
        # Enforce maximum physical radio buffer boundary constraint sizes (30 characters max)
        if length > 30:
            payload_bytes = payload_bytes[:30]
            length = 30
            
        # Compile the 4-byte structural packet header array block
        header = struct.pack(self.header_format, source_id, target_id, PACKET_TYPE_TEXT, length)
        return header + payload_bytes

    def deserialize_air_packet(self, raw_packet_bytes):
        """
        Intercepts incoming binary data arrays direct from the radio module 
        and extracts the clear variables matching gateway metrics.
        """
        if len(raw_packet_bytes) < 4:
            return None # Deformed fragment frame filter guard
            
        # Unpack the fixed header layout variables
        header_size = struct.calcsize(self.header_format)
        header_data = raw_packet_bytes[:header_size]
        source_id, target_id, packet_type, length = struct.unpack(self.header_format, header_data)
        
        payload_data = raw_packet_bytes[header_size:header_size + length]
        
        # Translate the binary variables into standard application readable objects
        if packet_type == PACKET_TYPE_TEXT:
            parsed_text = payload_data.decode('utf-8', errors='ignore')
            # Generate the string formatting frame template matching your gateway architecture hooks
            reconstructed_frame = f"[SRC:{source_id}][DST:{target_id}] {parsed_text}"
        elif packet_type == PACKET_TYPE_HANDSHAKE:
            reconstructed_frame = f"[SRC:{source_id}][DST:{target_id}] [SYS_INIT]: NODE_ONLINE"
        elif packet_type == PACKET_TYPE_VOICE:
            reconstructed_frame = f"[V_NOTE:#{source_id}:{length}]"
        else:
            reconstructed_frame = f"[SRC:{source_id}][DST:{target_id}] [RAW_DATA_HEX]: {payload_data.hex()}"
            
        return {
            "src": source_id,
            "dst": target_id,
            "type": packet_type,
            "length": length,
            "formatted_payload": reconstructed_frame
        }

if __name__ == "__main__":
    # Local unit parsing verification runtime test loops block execution check
    engine = OffGridPacketEngine()
    
    # Simulate serializing a standard message entry array sequence block
    print("\n[PACKET TEST] Encoding text string: 'RESCUE ME' from Node 996 to Server Base (Node 0)")
    binary_stream = engine.serialize_text_packet(16, 0, "RESCUE ME")
    print(f" -> Output Binary Raw Stream Array Hex: {binary_stream.hex().upper()}")
    
    # Simulate reverse execution pipeline extraction tracking parameters
    parsed_output = engine.deserialize_air_packet(binary_stream)
    print(f" -> Decoded Gateway Application Format Target: '{parsed_output['formatted_payload']}'")
