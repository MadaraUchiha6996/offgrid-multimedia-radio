import urllib.request
import json
import os
import time
from typing import Optional, List, Dict
from packet import RadioPacket

class OffGridInternetGateway:
    """
    Manages bridging between the offline radio mesh and the real-world internet.
    Runs on the central Raspberry Pi 4 base station.
    """
    def __init__(self, check_url: str = "https://google.com"):
        self.check_url = check_url
        self.internet_available = False
        self.last_check_time = 0.0
        self.check_interval = 10.0  # Check connectivity every 10 seconds

    def check_wan_connectivity(self) -> bool:
        """
        Performs a non-blocking hardware-free ping to verify if the 
        Raspberry Pi has an active WAN/Internet connection.
        """
        current_time = time.time()
        if current_time - self.last_check_time < self.check_interval:
            return self.internet_available

        self.last_check_time = current_time
        try:
            # Short timeout to prevent blocking the radio loop if line is dead
            urllib.request.urlopen(self.check_url, timeout=2.0)
            if not self.internet_available:
                print(" [Gateway Status] Internet connection detected! Gateway is fully active.")
            self.internet_available = True
        except Exception:
            if self.internet_available or self.last_check_time == current_time:
                print(" [Gateway Status] WAN Offline. Local internet links are severed. Switched to 100% Offline Mesh Mode.")
            self.internet_available = False
            
        return self.internet_available

    def route_radio_to_internet(self, packet: RadioPacket, decrypted_text: str) -> bool:
        """
        Attempts to push an emergency transmission out to real-world cloud APIs.
        Fails gracefully if the internet gateway is down.
        """
        is_online = self.check_wan_connectivity()
        
        if not is_online:
            print(f" [Gateway Drop] Cannot route message from Node {packet.source_node} to Internet. Base station is completely isolated.")
            return False

        print(f" [Gateway Forward] Success! Forwarding packet payload from Node {packet.source_node} to the web endpoint.")
        # Simulated Web API Post Routine:
        # payload = {"from_node": packet.source_node, "alert": decrypted_text, "timestamp": time.time()}
        # req = urllib.request.Request('https://emergency-service.org', data=json.dumps(payload).encode())
        return True

    def fetch_inbound_web_updates(self) -> List[Dict[str, any]]:
        """
        Polls a cloud broker server for any incoming messages or system notices 
        waiting to be sent down to the offline handsets.
        """
        if not self.check_wan_connectivity():
            return []

        print(" [Gateway Sync] Checking global cloud server for pending replies or external news feeds...")
        # Mocking an incoming server payload update structure
        try:
            mock_api_response = [
                {"target_node": 201, "message": "Base reply: Relief team dispatched to your sector grid."},
                {"target_node": 0xFFFF, "message": "Global Notice: Storm heading north. Stay under cover."}
            ]
            return mock_api_response
        except Exception:
            return []


# --- Local Gateway Sub-System Verification ---
if __name__ == "__main__":
    print("[*] Launching Internet Gateway Abstraction Layer validation...\n")
    
    gateway = OffGridInternetGateway()
    
    # 1. Run live check on your computer's active network link
    print("[*] Testing live WAN line interface link check...")
    status = gateway.check_wan_connectivity()
    print(f"    Current Link Status: {'ONLINE' if status else 'OFFLINE'}")
    
    # 2. Simulate a text message hitting the gateway boundary from an offline node
    from security import OffGridCipher
    cipher = OffGridCipher(key_phrase="DelhiOffGridEmergencyNetwork2026")
    
    msg = "Emergency Alert: Requesting WAN outward transmission."
    test_packet = RadioPacket(
        packet_type=RadioPacket.TYPE_TEXT,
        source_node=201,
        dest_node=1000, # Bound for server gateway
        packet_id=5,
        ttl=2,
        payload=cipher.process_payload(msg.encode('utf-8'))
    )
    
    # Run loopback routing check
    print("\n[*] Processing transit packet edge test...")
    gateway.route_radio_to_internet(test_packet, msg)
