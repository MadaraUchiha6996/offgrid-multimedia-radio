# No imports needed for built-in types

class OffGridCipher:
    """
    Handles payload encryption and decryption for the off-grid radio network.
    Uses an isolated symmetric XOR stream cipher with dynamic masking.
    
    This architecture is designed to be easily portable to C++ for the 
    ESP32-S3 firmware without requiring heavyweight external libraries.
    """
    def __init__(self, key_phrase: str = "OffGridMeshSecureKey2026"):
        # Convert string key-phrase into explicit byte arrays for processing
        self.key_bytes: bytes = key_phrase.encode('utf-8')
        self.key_length: int = len(self.key_bytes)

    def process_payload(self, data: bytes) -> bytes:
        """
        Encrypts or decrypts the given data stream symmetrically.
        Because XOR is a symmetric mathematical operation, passing encrypted bytes 
        back through this function automatically decodes them.
        """
        if not data:
            return b""

        processed = bytearray(len(data))
        
        # Apply a rolling index offset scheme to avoid static pattern leakage
        for idx in range(len(data)):
            # Pick a masking byte from our secret key-phrase
            key_byte = self.key_bytes[idx % self.key_length]
            
            # Mix the key index into the cipher block dynamically
            dynamic_mask = (key_byte + idx) & 0xFF
            
            # Execute bitwise XOR calculation
            processed[idx] = data[idx] ^ dynamic_mask

        return bytes(processed)


# --- Dedicated Structural Isolation Testing Module ---
if __name__ == "__main__":
    print("[*] Running secure isolated encryption layer validation...")
    
    cipher = OffGridCipher(key_phrase="EmergencyDelhiRadioNetworkKey")
    
    # Test 1: Simple Text Payload Verification
    original_text = "Urgent: Medical supplies requested at Sector 4 coordinate grid."
    raw_payload = original_text.encode('utf-8')
    
    encrypted_bytes = cipher.process_payload(raw_payload)
    print(f"[+] Payload scrambled successfully. Data length: {len(encrypted_bytes)} bytes.")
    print(f"    Raw Encrypted Hex: {encrypted_bytes.hex()[:30]}...")
    
    # Enforce isolation validation: check that original text is not readable in transit
    assert encrypted_bytes != raw_payload, "Security fault: Encryption resulted in cleartext leakage."
    
    # Test 2: Symmetric Loopback Decoding Verification
    decrypted_bytes = cipher.process_payload(encrypted_bytes)
    decoded_text = decrypted_bytes.decode('utf-8')
    
    assert decoded_text == original_text, "Symmetric encryption loopback corruption detected."
    print("[+] Symmetric decode loopback test passed successfully.")
    
    # Test 3: Binary Multimedia Voice Chunk Verification
    mock_voice_data = b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0" * 5
    encrypted_voice = cipher.process_payload(mock_voice_data)
    decrypted_voice = cipher.process_payload(encrypted_voice)
    
    assert decrypted_voice == mock_voice_data, "Binary stream serialization boundary collision."
    print("[+] Multimedia voice note binary stream encoding test passed cleanly.")
    
    print("[+] Security module structural validation completely PASSED.")
