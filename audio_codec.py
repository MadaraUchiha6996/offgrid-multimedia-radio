import struct

MAX_LEN = 240
FMT = "<HBBH"
H_SIZE = struct.calcsize(FMT)
chunks_dict = {}  # { msg_id: { chunk_idx: bytes } }


def make_packet(msg_id, idx, total, audio_data):
    if len(audio_data) > MAX_LEN:
        return b""  # Security/Validation: Guard rail retained
    return struct.pack(FMT, msg_id, idx, total, 0) + audio_data


def parse_packet(packet_bytes):
    if len(packet_bytes) < H_SIZE:
        return False, None

    m_id, idx, total, _ = struct.unpack(FMT, packet_bytes[:H_SIZE])

    # Replaces checking and creation logic natively
    msg_store = chunks_dict.setdefault(m_id, {})
    msg_store[idx] = packet_bytes[H_SIZE:]

    # One-liner sorted reassembly with built-in validation
    if len(msg_store) == total:
        if all(i in msg_store for i in range(total)):
            return True, chunks_dict.pop(m_id) and b"".join(
                msg_store[i] for i in range(total)
            )

    return False, None


if __name__ == "__main__":
    raw_voice = b"\xAA" * 600
    id_test, needed = 105, (len(raw_voice) + MAX_LEN - 1) // MAX_LEN

    stream = [
        make_packet(id_test, c, needed, raw_voice[c * MAX_LEN : (c + 1) * MAX_LEN])
        for c in range(needed)
    ]
    stream = [p for p in stream if p]

    for frame in stream:
        status, out = parse_packet(frame)

    print(
        "data transfer sequence complete."
        if (status and out == raw_voice)
        else "corrupted stream."
    )
