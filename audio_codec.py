import struct

# lora hardware packet constraints
MAX_LEN = 240
FMT = "<HBBH"
H_SIZE = struct.calcsize(FMT)

# holding chunks: { msg_id: { chunk_idx: bytes } }
chunks_dict = {}

def make_packet(msg_id, idx, total, audio_data):
    if len(audio_data) > MAX_LEN:
        print("packet too big for lora")
        return b""
    # 6-byte header prep ended with 2 bytes padding
    return struct.pack(FMT, msg_id, idx, total, 0) + audio_data

def parse_packet(packet_bytes):
    if len(packet_bytes) < H_SIZE:
        return False, None

    m_id, idx, total, _ = struct.unpack(FMT, packet_bytes[:H_SIZE])
    payload = packet_bytes[H_SIZE:]

    if m_id not in chunks_dict:
        chunks_dict[m_id] = {}

    chunks_dict[m_id][idx] = payload
    
    # check if we got all pieces
    if len(chunks_dict[m_id]) == total:
        full_audio = b""
        for i in range(total):
            if i not in chunks_dict[m_id]:
                return False, None
            full_audio += chunks_dict[m_id][i]
            
        del chunks_dict[m_id]
        return True, full_audio

    return False, None


if __name__ == "__main__":
    print("testing codec pipeline...")
    raw_voice = b"\xAA" * 600
    id_test = 105
    
    stream = []
    needed = (len(raw_voice) + MAX_LEN - 1) // MAX_LEN
    
    for count in range(needed):
        p = make_packet(id_test, count, needed, raw_voice[count*MAX_LEN : (count+1)*MAX_LEN])
        if p: stream.append(p)
            
    print(f"split into {len(stream)} frames.")
    
    status, out = False, None
    for frame in stream:
        status, out = parse_packet(frame)
        
    if status and out == raw_voice:
        print("data transfer sequence complete.")
    else:
        print("corrupted stream.")
