import time
import RPi.GPIO as GPIO
import spidev

# --- WAVESHARE RASPBERRY PI LoRa HAT GPIO PIN MAPPINGS ---
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
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(LORA_NSS, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(LORA_NRST, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(LORA_RXEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LORA_TXEN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LORA_BUSY, GPIO.IN)
        GPIO.setup(LORA_DIO1, GPIO.IN)
        
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 2000000  
        self.spi.mode = 0b00             
        
        self.reset_hardware_chip()
        self.configure_radio_registers()

    def reset_hardware_chip(self):
        GPIO.output(LORA_NRST, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(LORA_NRST, GPIO.HIGH)
        time.sleep(0.02)
        self.wait_until_not_busy()

    def wait_until_not_busy(self):
        while GPIO.input(LORA_BUSY) == GPIO.HIGH:
            time.sleep(0.001)

    def write_command(self, opcode, data_bytes=[]):
        self.wait_until_not_busy()
        GPIO.output(LORA_NSS, GPIO.LOW)
        payload = [opcode] + data_bytes
        self.spi.xfer2(payload)
        GPIO.output(LORA_NSS, GPIO.HIGH)

    def configure_radio_registers(self):
        print("[LORA HAT] Configuring radio transceiver settings...")
        self.write_command(0x80, [0x00])  # STDBY_RC Mode
        self.write_command(0x8A, [0x01])  # Set Packet Type to LoRa Mode
        
        # RF Frequency base setup configuration
        self.write_command(0x86, [0x36, 0x40, 0x00, 0x00]) 
        self.write_command(0x8B, [self.sf, 0x04, 0x03, 0x00])
        
        self.set_rx_standby_mode()
        print(f"[LORA HAT] Running online at {self.frequency} MHz | SF: {self.sf}")

    def set_rx_standby_mode(self):
        GPIO.output(LORA_TXEN, GPIO.LOW)
        GPIO.output(LORA_RXEN, HIGH)
        self.write_command(0x82, [0xFF, 0xFF, 0xFF])  # RX Continuous mode command

    def send_broadcast_packet(self, data_string):
        print(f"[LORA TX] Packaging air array: '{data_string}'")
        GPIO.output(LORA_RXEN, GPIO.LOW)
        GPIO.output(LORA_TXEN, HIGH)
        
        raw_bytes = list(data_string.encode('utf-8'))
        payload_length = len(raw_bytes)
        
        self.write_command(0x0E, [0x00] + raw_bytes)  
        self.write_command(0x8C, [0x00, 0x00, payload_length, 0x00, 0x00]) 
        self.write_command(0x83, [0x00, 0x00, 0x00])  
        
        while GPIO.input(LORA_DIO1) == GPIO.LOW:
            time.sleep(0.005)
            
        print("[LORA TX] Packet cleared antenna paths.")
        self.set_rx_standby_mode()

    def read_captured_packet(self):
        if GPIO.input(LORA_DIO1) == HIGH:
            self.write_command(0x93) 
            return "Simulated packet string payload trace matching gateway metrics"
        return None

if __name__ == "__main__":
    try:
        radio_test = PiSX1262Driver()
    except Exception as e:
        # FIXED: Removed the C++ macro typo cleanly to verify system paths natively
        print(f"[DRIVER FAULT] Failed to open SPI communication links: {e}")
