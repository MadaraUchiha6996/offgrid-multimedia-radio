import struct
from typing import Optional

class RadioPacket:
    """
    Handles serialization and deserialization of raw binary frames 
    transmitted over the off-grid mesh network.
    
    Byte Layout (Fixed 10-byte header + Variable Payload up to 246 bytes):
    -------------------------------------------------------------------------

    | Offset | Type   | Name             | Description                      |
    -------------------------------------------------------------------------

    | 0      | uint8  | magic_byte       | Protocol verification (0xA5)     |
    | 1      | uint8  | version          | Protocol version number          |
    | 2      | uint8  | packet_type      | VOICE, GPS, TEXT, REQ_MSG, etc.  |
    | 3      | uint8  | flags            | Bit 0: ACK Req, Bit 1: Encrypted |
    | 4-5    | uint16 | source_node      | ID of origin node                |
    | 6-7    | uint16 | dest_node        | ID of target node (0xFFFF = All) |
    | 8      | uint8  | packet_id        | Sequence tracking ID             |
    | 9      | uint8  | ttl              | Time To Live (Hop limit)         |
    | 10+    | bytes  | payload          | Application specific data        |
    -------------------------------------------------------------------------
    """
    MAGIC_BYTE = 0xA5
    HEADER_FORMAT = "<BBBBHHBB"  # Explicit little-endian mapping
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    MAX_FRAME_SIZE = 256

    # Packet Type Enums
    TYPE_TEXT    = 0x01
    TYPE_GPS     = 0x02
    TYPE_VOICE   = 0x03
    TYPE_REQ_MSG = 0x04
    TYPE_ACK     = 0x05

    def __init__(self, 
                 packet_type: int, 
                 source_node: int, 
                 dest_node: int, 
                 packet_id: int, 
                 ttl: int = 4, 
                 flags: int = 0, 
                 payload: bytes = b"",
                 version: int = 1):
        
        self.magic_byte: int = self.MAGIC_BYTE
        self.version: int = version
        self.packet_type: int = packet_type
        self.flags: int = flags
        self.source_node: int = source_node
        self.dest_node: int = dest_node
        self.packet_id: int = packet_id
        self.ttl: int = ttl
        self.payload: bytes = payload

    def serialize(self) -> bytes:
        if len(self.payload) > (self.MAX_FRAME_SIZE - self.HEADER_SIZE):
            raise ValueError(f"Payload size ({len(self.payload)}B) exceeds maximum limit.")

        header_bytes = struct.pack(
            self.HEADER_FORMAT,
            self.magic_byte,
            self.version,
            self.packet_type,
            self.flags,
            self.source_node,
            self.dest_node,
            self.packet_id,
            self.ttl
        )
        return header_bytes + self.payload

    @classmethod
    def deserialize(cls, raw_bytes: bytes) -> Optional['RadioPacket']:
        if len(raw_bytes) < cls.HEADER_SIZE:
            return None

        header_bytes = raw_bytes[:cls.HEADER_SIZE]
        payload_bytes = raw_bytes[cls.HEADER_SIZE:]

        try:
            unpacked = struct.unpack(cls.HEADER_FORMAT, header_bytes)
            magic, version, pkt_type, flags, src, dest, pkt_id, ttl = unpacked

            if magic != cls.MAGIC_BYTE:
                return None

            return cls(
                packet_type=pkt_type,
                source_node=src,
                dest_node=dest,
                packet_id=pkt_id,
                ttl=ttl,
                flags=flags,
                payload=payload_bytes,
                version=version
            )
        except struct.error:
            return None
