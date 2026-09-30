def process_payload(data, key_phrase="OffGridMeshSecureKey2026"):
    if not data:
        return b""
    k = key_phrase.encode("utf-8")
    # Native generator expression executes the index XOR mask on a single line
    return bytes(data[i] ^ ((k[i % len(k)] + i) & 0xFF) for i, _ in enumerate(data))


if __name__ == "__main__":
    key = "EmergencyDelhiRadioNetworkKey"
    text = "Urgent: Medical supplies requested at Sector 4 coordinate grid."

    enc = process_payload(text.encode("utf-8"), key)
    dec = process_payload(enc, key)

    print("Success" if dec.decode("utf-8") == text else "Error")
