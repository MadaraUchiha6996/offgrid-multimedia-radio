import struct

PACKET_TYPE_HANDSHAKE = 0x01  
PACKET_TYPE_TEXT      = 0x02  
PACKET_TYPE_VOICE     = 0x03  

class OffGridPacketEngine:
    def __init__(self):
        self.header_format = ">BBBB" 

    def serialize_text_packet(self, source_id, target_id, message_str):
        payload_bytes = message_str.encode('utf-8')
        length = len(payload_bytes)
        
        if length > 30:
            payload_bytes = payload_bytes[:30]
            length = 30
            
        header = struct.pack(self.header_format, source_id, target_id, PACKET_TYPE_TEXT, length)
        return header + payload_bytes

    def deserialize_air_packet(self, raw_packet_bytes):
        if len(raw_packet_bytes) < 4:
            return None 
            
        header_size = struct.calcsize(self.header_format)
        header_data = raw_packet_bytes[:header_size]
        source_id, target_id, packet_type, length = struct.unpack(self.header_format, header_data)
        payload_data = raw_packet_bytes[header_size:header_size + length]
        
        if packet_type == PACKET_TYPE_TEXT:
            parsed_text = payload_data.decode('utf-8', errors='ignore')
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
    engine = OffGridPacketEngine()
    binary_stream = engine.serialize_text_packet(16, 0, "RESCUE ME")
    parsed_output = engine.deserialize_air_packet(binary_stream)
    print(parsed_output['formatted_payload'])
