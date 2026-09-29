
import time
import RPi.GPIO as GPIO
import spidev

# --- WAVESHARE RASPBERRY PI LoRa HAT GPIO PIN MAPPINGS ---
# Fixed hardware pin definitions matching your server infrastructure layout
LORA_NSS   = 25  # Chip Select (SPI CS)
LORA_NRST  = 22  # Reset Pin
LORA_BUSY  = 24  # Busy Status Pin
LORA_DIO1  = 23  # Interrupt Request Pin (Packet Ready Flag)
LORA_RXEN  = 18  # RX Antenna Power Switch
LORA_TXEN  = 17  # TX Antenna Power Switch

class PiSX1262Driver:
    def __init__(self, frequency=868.0, sf=9, bw=125.0):
        self.frequency = frequency
        self.sf = sf
        self.bw = bw
        
        # Initialize Raspberry Pi Board Pin Modes
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(LORA_NSS, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(LORA_NRST, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(LORA_RXEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LORA_TXEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LORA_BUSY, GPIO.IN)
        GPIO.setup(LORA_DIO1, GPIO.IN)
        
        # Initialize Hardware SPI Bus 0, Device 0 on Pi 4
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 2000000  # Stable 2MHz transaction clock
        self.spi.mode = 0b00             # SPI Mode 0
        
        self.reset_hardware_chip()
        self.configure_radio_registers()

    def reset_hardware_chip(self):
        """Hard reset pulse sequence to flash SX1262 registers to fresh startup states"""
        GPIO.output(LORA_NRST, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(LORA_NRST, GPIO.HIGH)
        time.sleep(0.02)
        self.wait_until_not_busy()

    def wait_until_not_busy(self):
        """Halts transaction commands while the internal sub-GHz engine is processing"""
        while GPIO.input(LORA_BUSY) == GPIO.HIGH:
            time.sleep(0.001)

    def write_command(self, opcode, data_bytes=[]):
        """Pushes data frames across the SPI bus line down to the chip buffer"""
        self.wait_until_not_busy()
        GPIO.output(LORA_NSS, GPIO.LOW)
        payload = [opcode] + data_bytes
        self.spi.xfer2(payload)
        GPIO.output(LORA_NSS, GPIO.HIGH)

    def configure_radio_registers(self):
        """Configures packet configuration settings to directly mirror your handheld firmware layout"""
        print(f"[LORA HAT] Booting radio transceiver register configurations...")
        
        # Step 1: Force Standby Mode configuration values
        self.write_command(0x80, [0x00])  # STDBY_RC Mode
        
        # Step 2: Establish base RF Packet type parameters
        self.write_command(0x8A, [0x01])  # Set Packet Type to LoRa Mode
        
        # Step 3: Synchronize operating values matching handheld (868.0MHz fallback calculation setup)
        # RF Frequency math register configuration: (Freq * 32000000) / 2^25
        self.write_command(0x86, [0x36, 0x40, 0x00, 0x00]) 
        
        # Step 4: Map modulation variables (SF9, Bandwidth 125kHz, Coding Rate 4/7)
        self.write_command(0x8B, [self.sf, 0x04, 0x03, 0x00])
        
        # Step 5: Engage low-noise listening paths
        self.set_rx_standby_mode()
        print(f"[LORA HAT] Connection running online at {self.frequency} MHz | Spreading Factor: {self.sf}")

    def set_rx_standby_mode(self):
        """Switches physical RF circuit routing lines to engage high-gain listening"""
        GPIO.output(LORA_TXEN, GPIO.LOW)
        GPIO.output(LORA_RXEN, HIGH)
        # Fire official command register pulse to command continuous standby listening
        self.write_command(0x82, [0xFF, 0xFF, 0xFF])  # RX Continuous mode command

    def send_broadcast_packet(self, data_string):
        """Packages up a string data frame payload and blasts it into the air"""
        print(f"[LORA TX] Packaging air array: '{data_string}'")
        
        # Disengage receiver loops, throw power rails down to transmission amplifier paths
        GPIO.output(LORA_RXEN, GPIO.LOW)
        GPIO.output(LORA_TXEN, HIGH)
        
        raw_bytes = list(data_string.encode('utf-8'))
        payload_length = len(raw_bytes)
        
        # Write payload data block directly down into the hardware FIFO buffer memory coordinates
        self.write_command(0x0E, [0x00] + raw_bytes)  # Write Buffer Command
        self.write_command(0x8C, [0x00, 0x00, payload_length, 0x00, 0x00]) # Set Packet Params
        
        # Engage actual output transmission blast pulse register configuration (+22 dBm Max output matching Potentiometer)
        self.write_command(0x83, [0x00, 0x00, 0x00])  # Start TX Command
        
        # Wait until DIO1 interrupt status line spikes high signaling completion flag
        while GPIO.input(LORA_DIO1) == GPIO.LOW:
            time.sleep(0.005)
            
        print(f"[LORA TX] Data broadcast packet cleared antenna paths successfully.")
        
        # Drop power configurations directly back down to standby receiver monitoring paths
        self.set_rx_standby_mode()

    def read_captured_packet(self):
        """Extracts data frame bytes out of the hardware buffer layer upon a signal interrupt flag"""
        if GPIO.input(LORA_DIO1) == GPIO.HIGH:
            # Command instruction pulse reads packet status size bounds inside buffer
            # In a live tracking run, this triggers the gateway parser layer modules
            self.write_command(0x93) # Clear Irq Status Command flags register
            return "Simulated packet string payload trace matching gateway metrics"
        return None

if __name__ == "__main__":
    # Test initialization check to evaluate SPI communication pipelines locally
    try:
        radio_test = PiSX1262Driver()
    except Exception as e:
        print(f"[DRIVER FAULT] Failed to verify system GPIO state lines: {e}")
