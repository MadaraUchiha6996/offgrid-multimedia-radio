import struct

# Unified Little-Endian format to match the ESP32-S3 radio links
FMT = "<BBBB"
TYPES = {0x01: "[SYS_INIT]: NODE_ONLINE", 0x02: "{}", 0x03: None}


def serialize_text_packet(src, dst, msg):
    payload = msg.encode("utf-8")[:30]
    return struct.pack(FMT, src, dst, 0x02, len(payload)) + payload


def deserialize_air_packet(raw):
    if len(raw) < 4:
        return None

    src, dst, p_type, length = struct.unpack(FMT, raw[:4])
    pay = raw[4 : 4 + length]

    fmt = TYPES.get(p_type, f"[RAW_DATA_HEX]: {pay.hex()}")
    if p_type == 0x02:
        fmt = fmt.format(pay.decode("utf-8", errors="ignore"))
    elif p_type == 0x03:
        fmt = f"[V_NOTE:#{src}:{length}]"

    return {
        "src": src,
        "dst": dst,
        "type": p_type,
        "length": length,
        "formatted_payload": (
            fmt if p_type in (0x01, 0x03) else f"[SRC:{src}][DST:{dst}] {fmt}"
        ),
    }


if __name__ == "__main__":
    # Internal test pipeline
    stream = serialize_text_packet(16, 0, "RESCUE ME")
    print(deserialize_air_packet(stream)["formatted_payload"])
