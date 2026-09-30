import struct
from packet import RadioPacket

bulletins = {}  # Cache storage for downlinked alerts


def parse_satellite_transport_packet(stream_bytes):
    if len(stream_bytes) < 3:
        return None
    try:
        f_id, length = struct.unpack("<HB", stream_bytes[:3])
        bulletins[f_id] = stream_bytes[3 : 3 + length].decode("utf-8", errors="ignore")
        return f_id, bulletins[f_id]
    except struct.error:
        return None


def package_for_mesh_request(feed_id, requestor_node, current_packet_id):
    if feed_id not in bulletins:
        return None

    # Inline truncation to strict 240-byte LoRa packet window size constraints
    return RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=1000,
        dest_node=requestor_node,
        packet_id=current_packet_id,
        ttl=4,
        flags=0x02,
        payload=bulletins[feed_id].encode("utf-8")[:240],
    )


if __name__ == "__main__":
    mock_id, text = 0x88A1, "ALERT: Water distribution center open at Sector 6. Supply stable."
    payload = text.encode("utf-8")
    stream = struct.pack("<HB", mock_id, len(payload)) + payload

    res = parse_satellite_transport_packet(stream)
    assert res is not None

    pkt = package_for_mesh_request(0x88A1, 201, 44)
    assert pkt and pkt.dest_node == 201
    print(f"[+] RadioPacket generated cleanly. Size: {len(pkt.serialize())} bytes.")
