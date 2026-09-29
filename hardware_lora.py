import time
from typing import Optional

# These libraries run natively on the Raspberry Pi. 
# We use try/except block formatting so the code won't crash when testing on your laptop!
try:
    import RPi.GPIO as GPIO
    import spidev
    HARDWARE_MODE = True
except ImportError:
    HARDWARE_MODE = False
    print("[!] GPIO/SPI libraries not found. Falling back to Hardware Emulation Mode.")

class SX1262HardwareWrapper:
    """
    Low-level SPI and GPIO translation layer for the Waveshare SX1262 LoRa HAT.
    Replaces the virtual simulation queues with physical hardware register tracking.
    
    Standard Waveshare Pi 4 Jumper Wire Pin Mapping:
    ---------------------------------------------------------

    | Pin Name | Pi 4 GPIO Pin | Description                |
    ---------------------------------------------------------

    | MOSI     | GPIO 10 (Pin 19)| SPI Data Out to HAT      |
    | MISO     | GPIO 9  (Pin 21)| SPI Data In from HAT     |
    | SCK      | GPIO 11 (Pin 23)| SPI Clock Line           |
    | NSS/CS   | GPIO 8  (Pin 24)| SPI Chip Select (CE0)    |
    | BUSY     | GPIO 24 (Pin 18)| HAT Busy Status Indicator|
    | RST      | GPIO 22 (Pin 15)| HAT Physical Reset Line  |
    | DIO1     | GPIO 25 (Pin 22)| Packet RX/TX Interrupt   |
    ---------------------------------------------------------
    """
    def __init__(self, bus: int = 0, device: int = 0, pin_busy: int = 24, pin_rst: int = 22, pin_dio1: int = 25):
        self.bus = bus
        self.device = device
        self.pin_busy = pin_busy
        self.pin_rst = pin_rst
        self.pin_dio1 = pin_dio1
        
        if HARDWARE_MODE:
            self._initialize_pins()
            self._initialize_spi()
        else:
            print("[Mock Hardware] Initialized dummy registers for SPI Bus 0, Device 0.")

    def _initialize_pins(self):
        """Configures the physical Pi 4 hardware pins using BCM GPIO indexing."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup output lines
        GPIO.setup(self.pin_rst, GPIO.OUT)
        
        # Setup input lines from the Semtech SX1262 chip triggers
        GPIO.setup(self.pin_busy, GPIO.IN, pull_up_down=GPIO.PUD_NONE)
        GPIO.setup(self.pin_dio1, GPIO.IN, pull_up_down=GPIO.PUD_NONE)
        
        # Trigger hard reset pulse sequence to clear chip state registers
        GPIO.output(self.pin_rst, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(self.pin_rst, GPIO.HIGH)
        time.sleep(0.02)
        print("[Hardware] GPIO pins configured. Hardware reset sequence sent down jumper wires.")

    def _initialize_spi(self):
        """Configures the hardware clock speeds and mode bits for the radio link."""
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 2000000  # 2 MHz clock speed is optimal for short jumper wire setups
        self.spi.mode = 0b00             # Semtech chips utilize standard SPI Mode 0
        print("[Hardware] SPI Peripheral linked successfully.")

    def wait_until_not_busy(self):
        """Blocks execution threads safely while the radio chip is internal-processing."""
        if not HARDWARE_MODE:
            return
        # Infinite loop protection helper variable
        timeout = time.time() + 1.0
        while GPIO.input(self.pin_busy) == GPIO.HIGH:
            if time.time() > timeout:
                print("[⚠️ Hardware Warning] SX1262 device stuck in busy lock status state.")
                break
            time.sleep(0.001)

    def write_command(self, opcode: int, data_bytes: list[int]):
        """Pushes a functional operation command frame over the SPI MOSI line."""
        if not HARDWARE_MODE:
            return
        
        self.wait_until_not_busy()
        # Compile opcode combined frame layout block matrix
        tx_buffer = [opcode] + data_bytes
        
        # SpiDev automatically drives the NSS/CS line low during transactional transfers
        self.spi.xfer2(tx_buffer)

    def read_command(self, opcode: int, num_bytes_to_read: int) -> list[int]:
        """Requests status tracking data fields back across the SPI MISO line."""
        if not HARDWARE_MODE:
            # Emulated default success responses
            return [0x00] * num_bytes_to_read

        self.wait_until_not_busy()
        
        # Semtech SX1262 command formatting mandates a dummy status byte during read requests
        tx_buffer = [opcode, 0x00] + ([0x00] * num_bytes_to_read)
        rx_buffer = self.spi.xfer2(tx_buffer)
        
        # Slice off opcode and dummy status responses before processing down the stack
        return rx_buffer[2:]

# --- Local Component Isolation Checking ---
if __name__ == "__main__":
    print("[*] Running Hardware SPI Adapter Verification Protocol...\n")
    
    # Spin up our driver class
    radio_modem = SX1262HardwareWrapper()
    
    # Test a dummy read command parameter check (e.g. Opcode 0x11 fetches the current device error status logs)
    print("[*] Simulating device register query...")
    status_bytes = radio_modem.read_command(opcode=0x11, num_bytes_to_read=2)
    print(f"[+] Operational transaction cycle processed. Extracted registers response block: {status_bytes}")
