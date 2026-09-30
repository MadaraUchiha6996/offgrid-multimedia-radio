import time
import sys
from database import init_vaults
from hardware_lora import PiSX1262Driver
from routing import MeshNetworkRouter
from gateway import parse_incoming_radio_frame
from packet import OffGridPacketEngine

class OffGridMasterServer:
    def __init__(self):
        init_vaults()
        self.router = MeshNetworkRouter()
        self.packet_decoder = OffGridPacketEngine()
        
        try:
            self.radio = PiSX1262Driver(frequency=868.0, sf=9, bw=125.0)
            self.hardware_active = True
        except Exception as e:
            self.hardware_active = False

    def start_server_loop(self):
        try:
            while True:
                raw_packet_data = None
                rssi_signal = -120.0
                snr_quality = 0.0
                
                if self.hardware_active:
                    raw_packet_data = self.radio.read_captured_packet()
                    if raw_packet_data:
                        rssi_signal = -64.0
                        snr_quality = 8.5
                else:
                    time.sleep(5)
                    raw_packet_data = "[SRC:996][DST:SERVER] [SYS_INIT]: NODE_ONLINE"
                    rssi_signal = -64.2
                    snr_quality = 9.0

                if raw_packet_data:
                    self.router.ingress_packet(raw_packet_data, rssi_signal, snr_quality)
                    active_job = self.router.process_next_packet()
                    
                    if active_job:
                        parse_incoming_radio_frame(
                            active_job["payload"], 
                            active_job["rssi"], 
                            active_job["snr"]
                        )
                        
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    server_terminal = OffGridMasterServer()
    server_terminal.start_server_loop()
