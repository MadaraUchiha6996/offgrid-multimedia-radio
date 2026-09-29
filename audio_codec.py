import struct
from typing import List, Dict, Optional, Tuple

class AudioStreamChunk:
    """
    Handles the structural packaging of individual digitized audio fragments.
    
    Byte Layout (Fixed 6-byte header + Variable Audio Data up to 240 bytes):
    -------------------------------------------------------------------------

    | Offset | Type   | Name             | Description                      |
    -------------------------------------------------------------------------

    | 0-1    | uint16 | message_id       | Unique ID linking this voice note|
    | 2      | uint8  | chunk_index      | Current chunk sequence number    |
    | 3      | uint8  | total_chunks     | Total chunks required to solve   |
    | 4-5    | uint16 | reserved         | Padding for memory alignment     |
    | 6+     | bytes  | audio_bytes      | Ultra-compressed voice bytes     |
    -------------------------------------------------------------------------
    """
    HEADER_FORMAT = "<HBBH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    MAX_CHUNK_PAYLOAD = 240

    def __init__(self, message_id: int, chunk_index: int, total_chunks: int, audio_bytes: bytes):
        self.message_id: int = message_id
        self.chunk_index: int = chunk_index
        self.total_chunks: int = total_chunks
        self.audio_bytes: bytes = audio_bytes

    def serialize(self) -> bytes:
        """Packs the stream fragment headers and audio payload into binary format."""
        if len(self.audio_bytes) > self.MAX_CHUNK_PAYLOAD:
            raise ValueError(f"Audio payload chunk size ({len(self.audio_bytes)}B) exceeds structural limit.")
        
        header = struct.pack(self.HEADER_FORMAT, self.message_id, self.chunk_index, self.total_chunks, 0)
        return header + self.audio_bytes

    @classmethod
    def deserialize(cls, data: bytes) -> Optional['AudioStreamChunk']:
        """Decodes raw binary fragments back into an organized stream chunk object."""
        if len(data) < cls.HEADER_SIZE:
            return None
        try:
            msg_id, index, total, _ = struct.unpack(cls.HEADER_FORMAT, data[:cls.HEADER_SIZE])
            audio_payload = data[cls.HEADER_SIZE:]
            return cls(message_id=msg_id, chunk_index=index, total_chunks=total, audio_bytes=audio_payload)
        except struct.error:
            return None


class AudioReassembler:
    """
    Assembles incoming fragmented radio audio bytes back into unified voice files.
    """
    def __init__(self):
        # Tracks active incoming transfers: message_id -> {chunk_index: audio_bytes}
        self.transfer_buffers: Dict[int, Dict[int, bytes]] = {}

    def add_chunk(self, chunk: AudioStreamChunk) -> Tuple[bool, Optional[bytes]]:
        """
        Ingests a new audio frame into the tracking sequence matrix.
        
        Returns:
            Tuple[is_complete, full_audio_bytes_if_complete]
        """
        if chunk.message_id not in self.transfer_buffers:
            self.transfer_buffers[chunk.message_id] = {}

        # Add fragment to specific index mapping
        self.transfer_buffers[chunk.message_id][chunk.chunk_index] = chunk.audio_bytes
        
        # Verify if all parts have arrived
        active_buffer = self.transfer_buffers[chunk.message_id]
        if len(active_buffer) == chunk.total_chunks:
            # Reconstruct the jigsaw sequence array smoothly
            full_voice_note = b""
            for i in range(chunk.total_chunks):
                full_voice_note += active_buffer[i]
            
            # Clear historical storage map to free up local memory footprint
            del self.transfer_buffers[chunk.message_id]
            return True, full_voice_note

        return False, None


# --- Structural Unit Sanity Validation Test ---
if __name__ == "__main__":
    print("[*] Running Voice Note chunking & encoder validation routines...")
    
    # Simulate an ultra-compressed 10-second voice payload (e.g. 600 bytes of Codec2 data)
    mock_10s_voice_note = b"\xAA" * 600
    msg_id = 99
    
    # --- Chunking Simulation ---
    chunks_list: List[bytes] = []
    chunk_size = AudioStreamChunk.MAX_CHUNK_PAYLOAD
    total_needed = (len(mock_10s_voice_note) + chunk_size - 1) // chunk_size
    
    for idx in range(total_needed):
        start = idx * chunk_size
        end = start + chunk_size
        audio_slice = mock_10s_voice_note[start:end]
        
        chunk_obj = AudioStreamChunk(message_id=msg_id, chunk_index=idx, total_chunks=total_needed, audio_bytes=audio_slice)
        chunks_list.append(chunk_obj.serialize())
        
    print(f"[+] Successfully sliced voice note into {len(chunks_list)} individual binary packets.")
    
    # --- Reassembly Simulation ---
    assembler = AudioReassembler()
    is_done = False
    reconstructed_data = None
    
    for raw_chunk in chunks_list:
        parsed_chunk = AudioStreamChunk.deserialize(raw_chunk)
        assert parsed_chunk is not None, "Failed to parse chunk signature frame data."
        is_done, reconstructed_data = assembler.add_chunk(parsed_chunk)
        
    assert is_done is True, "Reassembly sequence state machine failed completion test."
    assert reconstructed_data == mock_10s_voice_note, "Audio integrity loss detected during merge."
    
    print("[+] All structural audio reassembler integrity verifications PASSED cleanly.")
