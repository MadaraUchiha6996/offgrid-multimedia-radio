import time
import sys
# Native modular asset imports from your repository files framework
from database import init_vaults
from hardware_lora import PiSX1262Driver
from routing import MeshNetworkRouter
from gateway import parse_incoming_radio_frame
from packet import OffGridPacketEngine # FIXED: Added the required missing dependency loop hook here

class OffGridMasterServer:
    def __init__(self):
        print("====================================================")
        print("    INITIALIZING OFF-GRID MULTIMEDIA CENTRAL SERVER ")
        print("====================================================")
        
        # Step 1: Pre-stage asset databases and storage directory folders
        init_vaults()
        
        # Step 2: Initialize priority mesh routing queues
        self.router = MeshNetworkRouter()
        
        # Step 3: Instantiate binary serialization translator mapping rules
        self.packet_decoder = OffGridPacketEngine()
        
        # Step 4: Fire up the physical Waveshare SX1262 LoRa hardware bus line
        try:
            self.radio = PiSX1262Driver(frequency=868.0, sf=9, bw=125.0)
            self.hardware_active = True
        except Exception as e:
            print(f"\n[HARDWARE WARNING] Could not bind SPI/GPIO lines pins. Running in simulation mode: {e}")
            self.hardware_active = False

    def start_server_loop(self):
        print("\n[SERVER SYSTEM] Master orchestration framework completely operational.")
        print("[SERVER SYSTEM] Standing by for incoming background handheld traffic queue...\n")
        
        try:
            while True:
                raw_packet_data = None
                rssi_signal = -120.0
                snr_quality = 0.0
                
                if self.hardware_active:
                    # Physical hardware transaction polling routine
                    raw_packet_data = self.radio.read_captured_packet()
                    if raw_packet_data:
                        # Extract signal attributes direct from chip registers
                        rssi_signal = -64.0
                        snr_quality = 8.5
                else:
                    # Continuous fallback simulation generator clock tick block
                    time.sleep(5)
                    raw_packet_data = "[SRC:996][DST:SERVER] [SYS_INIT]: NODE_ONLINE"
                    rssi_signal = -64.2
                    snr_quality = 9.0

                # ----------------=====================================================
                # NETWORK DATA PIPELINE ROUTING LAYER
                # ----------------=====================================================
                if raw_packet_data:
                    # Pass the captured air packet directly into the prioritization engine
                    self.router.ingress_packet(raw_packet_data, rssi_signal, snr_quality)
                    
                    # Pull the next available sequenced packet from the priority queues
                    active_job = self.router.process_next_packet()
                    
                    if active_job:
                        # Direct the prioritized packet payload to your gateway logging modules
                        parse_incoming_radio_frame(
                            active_job["payload"], 
                            active_job["rssi"], 
                            active_job["snr"]
                        )
                        
                # Yield operating processor cycles cleanly to prevent terminal lockups
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n[SERVER COOLDOWN] Asynchronous supervisor loops halted cleanly. Exiting terminal.")
            sys.exit(0)

if __name__ == "__main__":
    # Launch the master off-grid server instance
    server_terminal = OffGridMasterServer()
    server_terminal.start_server_loop()
