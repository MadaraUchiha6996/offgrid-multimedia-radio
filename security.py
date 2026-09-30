class OffGridCipher:
    def __init__(self, key_phrase="OffGridMeshSecureKey2026"):
        self.key_bytes = key_phrase.encode('utf-8')
        self.key_length = len(self.key_bytes)

    def process_payload(self, data):
        if not data:
            return b""

        processed = bytearray(len(data))
        for idx in range(len(data)):
            key_byte = self.key_bytes[idx % self.key_length]
            dynamic_mask = (key_byte + idx) & 0xFF
            processed[idx] = data[idx] ^ dynamic_mask

        return bytes(processed)

if __name__ == "__main__":
    cipher = OffGridCipher("EmergencyDelhiRadioNetworkKey")
    original_text = "Urgent: Medical supplies requested at Sector 4 coordinate grid."
    raw_payload = original_text.encode('utf-8')
    
    encrypted_bytes = cipher.process_payload(raw_payload)
    decrypted_bytes = cipher.process_payload(encrypted_bytes)
    
    if decrypted_bytes.decode('utf-8') == original_text:
        print("Success")
    else:
        print("Error")
