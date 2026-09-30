import struct

BEACON_FMT, GPS_FMT = "<HBBff", "<ff"


# --- System Beacon Serialization ---
def pack_beacon(server_node_id, network_chan, flags, lat, lon):
    return struct.pack(BEACON_FMT, server_node_id, network_chan, flags, lat, lon)


def unpack_beacon(data):
    try:
        return struct.unpack(BEACON_FMT, data[:12]) if len(data) >= 12 else None
    except struct.error:
        return None


# --- GPS Payload Serialization ---
def pack_gps(lat, lon):
    return struct.pack(GPS_FMT, lat, lon)


def unpack_gps(data):
    try:
        return struct.unpack(GPS_FMT, data[:8]) if len(data) >= 8 else None
    except struct.error:
        return None
