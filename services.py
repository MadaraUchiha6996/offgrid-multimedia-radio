import struct

class SystemBeaconPayload:
    FORMAT = "<HBBff"
    SIZE = struct.calcsize(FORMAT)

    FLAG_INTERNET_GATEWAY = 1 << 0
    FLAG_SATELLITE_DISH   = 1 << 1

    def __init__(self, server_node_id, network_chan, flags, lat, lon):
        self.server_node_id = server_node_id
        self.network_chan = network_chan
        self.flags = flags
        self.lat = lat
        self.lon = lon

    def serialize(self):
        return struct.pack(
            self.FORMAT, 
            self.server_node_id, 
            self.network_chan, 
            self.flags, 
            self.lat, 
            self.lon
        )

    @classmethod
    def deserialize(cls, data):
        if len(data) < cls.SIZE:
            return None
        try:
            unpacked = struct.unpack(cls.FORMAT, data[:cls.SIZE])
            return cls(unpacked[0], unpacked[1], unpacked[2], unpacked[3], unpacked[4])
        except struct.error:
            return None


class GPSPayload:
    FORMAT = "<ff"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        return struct.pack(self.FORMAT, self.latitude, self.longitude)

    @classmethod
    def deserialize(cls, data):
        if len(data) < cls.SIZE:
            return None
        try:
            lat, lon = struct.unpack(cls.FORMAT, data[:cls.SIZE])
            return cls(lat, lon)
        except struct.error:
            return None
