import sys
import time
from database import init_vaults
from gateway import parse_incoming_radio_frame
from hardware_lora import PiSX1262Driver
from routing import MeshNetworkRouter


class OffGridMasterServer:

    def __init__(self):
        init_vaults()
        self.router = MeshNetworkRouter()
        try:
            self.radio = PiSX1262Driver(frequency=868.0, sf=9, bw=125.0)
        except Exception:
            self.radio = None  # Replaces booleans with native object existence

    def start_server_loop(self):
        while True:
            # Inline conditional handles hardware vs simulated fallback data
            if self.radio:
                data = self.radio.read_captured_packet()
                rssi, snr = -64.0, 8.5 if data else (-120.0, 0.0)
            else:
                time.sleep(5)
                data, rssi, snr = "[SRC:996][DST:SERVER] [SYS_INIT]: NODE_ONLINE", -64.2, 9.0

            if data:
                self.router.ingress_packet(data, rssi, snr)
                job = self.router.process_next_packet()
                if job:
                    # Native unpacking mapping to function args
                    parse_incoming_radio_frame(job["payload"], job["rssi"], job["snr"])

            time.sleep(0.01)


if __name__ == "__main__":
    try:
        OffGridMasterServer().start_server_loop()
    except KeyboardInterrupt:
        sys.exit(0)  # Handles process safety globally at the execution entry point
