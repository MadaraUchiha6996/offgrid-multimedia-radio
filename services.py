import struct
from typing import Optional

class SystemBeaconPayload:
    """
    Handles serialization of the server's discovery heartbeat broadcast.
    Allows ESP32 handsets to automatically view available networks.
    
    Byte Layout (Fixed 12 bytes):
    ----------------------------------------------------------------------

    | Offset | Type   | Name          | Description                       |
    ----------------------------------------------------------------------

    | 0-1    | uint16 | server_node_id| Explicit network ID of the server |
    | 2      | uint8  | network_chan  | Active LoRa sub-channel frequency |
    | 3      | uint8  | flags         | Bit 0: Has Internet, Bit 1: Dish  |
    | 4-7    | float  | server_lat    | Server location latitude          |
    | 8-11   | float  | server_lon    | Server location longitude         |
    ----------------------------------------------------------------------
    """
    FORMAT = "<HBBff"
    SIZE = struct.calcsize(FORMAT)

    FLAG_INTERNET_GATEWAY = 1 << 0
    FLAG_SATELLITE_DISH   = 1 << 1

    def __init__(self, server_node_id: int, network_chan: int, flags: int, lat: float, lon: float):
        self.server_node_id: int = server_node_id
        self.network_chan: int = network_chan
        self.flags: int = flags
        self.lat: float = lat
        self.lon: float = lon

    def serialize(self) -> bytes:
        return struct.pack(
            self.FORMAT, 
            self.server_node_id, 
            self.network_chan, 
            self.flags, 
            self.lat, 
            self.lon
        )

    @classmethod
    def deserialize(cls, data: bytes) -> Optional['SystemBeaconPayload']:
        if len(data) < cls.SIZE:
            return None
        try:
            unpacked = struct.unpack(cls.FORMAT, data[:cls.SIZE])
            return cls(
                server_node_id=unpacked[0],
                network_chan=unpacked[1],
                flags=unpacked[2],
                lat=unpacked[3],
                lon=unpacked[4]
            )
        except struct.error:
            return None


class GPSPayload:
    """
    Compressed 8-byte coordinate representation for active tracking.
    
    Byte Layout (Fixed 8 bytes):
    ----------------------------------------------------------------------

    | Offset | Type   | Name      | Description                           |
    ----------------------------------------------------------------------

    | 0-3    | float  | latitude  | GPS Latitude coordinate               |
    | 4-7    | float  | longitude | GPS Longitude coordinate              |
    ----------------------------------------------------------------------
    """
    FORMAT = "<ff"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude

    def serialize(self) -> bytes:
        return struct.pack(self.FORMAT, self.latitude, self.longitude)

    @classmethod
    def deserialize(cls, data: bytes) -> Optional['GPSPayload']:
        if len(data) < cls.SIZE:
            return None
        try:
            lat, lon = struct.unpack(cls.FORMAT, data[:cls.SIZE])
            return cls(latitude=lat, longitude=lon)
        except struct.error:
            return None
