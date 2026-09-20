import serial
import sqlite3
import time
import sys

# Configure hardware serial communication link to the ESP32-S3 via USB data cable
SERIAL_PORT = '/dev/ttyACM0'  # Default port for USB serial devices on Raspberry Pi Linux
BAUD_RATE = 115200

# Initialize localized SQLite text logs database framework
def init_database():
    try:
        connection = sqlite3.connect('radio_network.db')
        cursor = connection.cursor()
        # Create a clean table structure to serialize incoming message data packets
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                direction TEXT,
                payload TEXT
            )
        ''')
        connection.commit()
        connection.close()
        print("Local SQLite Message Database Initialized Successfully.")
    except Exception as error:
        print(f"Database Initialization Error: {error}")
        sys.exit(1)

# Log verified message strings directly down into the database storage layer
def log_message(direction, payload):
    try:
        connection = sqlite3.connect('radio_network.db')
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO chat_logs (direction, payload) VALUES (?, ?)", 
            (direction, payload)
        )
        connection.commit()
        connection.close()
        print(f"[{direction}] Logged: {payload}")
    except Exception as error:
        print(f"Error Logging Payload to Local Database: {error}")

def main():
    init_database()
    
    print(f"Opening Serial Link on {SERIAL_PORT} at {BAUD_RATE} baud...")
    try:
        # Open data line connection stream
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        # Flush the buffer memory lines to prevent reading historic startup noise
        ser.flush()
        print("Serial Interface Line Established. Monitoring Network State...")
    except serial.SerialException:
        print(f"Warning: Could not open {SERIAL_PORT}. Check physical USB-A to USB-C link.")
        print("Running in Simulation Mode for design verification...")
        ser = None

    while True:
        try:
            # 1. Listen for data frames arriving from the ESP32 co-processor board link
            if ser and ser.in_waiting > 0:
                raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Check for the matching typing interface header code we set up in C++
                if raw_line.startswith("TX_DATA:"):
                    message_payload = raw_line.replace("TX_DATA:", "")
                    print(f"\n>> Received Text from Handset Handset Matrix: {message_payload}")
                    
                    # Log data into the system file
                    log_message("SENT", message_payload)
                    
                    # Future integration milestone step:
                    # This is where the Pi passes the string to the Waveshare LoRa HAT 
                    # to fire the Sub-GHz radio waves across the neighborhood grid.
            
            # 2. Allow typing input entries straight from the base terminal screen prompt
            # (Simulation fallback interface tool)
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print("\nShutting Down Local Linux Host Router Service. Closing Connections.")
            if ser:
                ser.close()
            break

if __name__ == '__main__':
    main()
