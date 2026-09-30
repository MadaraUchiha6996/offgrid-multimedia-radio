# DIY Off-Grid Radio Network for emergencies 

So basically this project is an offline communication setup meant for disasters when standard internet and cell towers go completely dark. It uses a main home base station linked to small portable handheld walkie-talkie units. They talk over raw radio waves without needing any active sim cards, wifi, or external provider networks.

### how the system layout works

The whole thing splits into two main sections that connect automatically:
1. **The Handheld Walkie-Talkie (ESP32-S3):** This takes your voice notes through an I2S mic, shows details on a small OLED display screen, and lets you type out messages using a simple button menu. 
2. **The Central Home Server Hub (Raspberry Pi 4):** This stays running at home 24/7 to sort out incoming radio signals, handle emergency message priorities, and save everything into a local SQLite database storage vault.

---

## repository file guide

*   `offgrid_radio_node.ino` — Master C++ code running on the portable ESP32-S3 handsets.
*   `main_server.py` — The main supervisor loop running on the home base station.
*   `hardware_lora.py` — Simple python driver to talk to the Waveshare LoRa radio module over SPI pins.
*   `gateway.py` — Extracts packets from incoming strings and handles data filtering.
*   `routing.py` — The code that sorts out message queues so emergency alerts go first.
*   `database.py` — Simple SQL layout that holds text history and voice logs.
*   `audio_codec.py` — Compresses voice recordings so they can fit through tiny radio bands.

---

### main operational features

*   **Priority message waking:** If a critical emergency broadcast comes in while the radio is quiet, the handset breaks its standby loop instantly. It turns on the hardware, plays a quick dual-tone buzzer alert tone, and flashes a small envelope graphic on the screen for 4 seconds.
*   **6-minute power saver mode:** If you don't click any buttons for 6 minutes (360,000 milliseconds), the ESP32 automatically cuts off power to the OLED screen panel registry. This keeps it from killing your power bank battery, leaving only the LoRa chip listening quietly for incoming signals.
*   **Rough range tracking without gps:** Option 3 on the menu checks raw signal quality stats (RSSI and SNR values) and calculates them through a basic logarithmic formula. This gives you a rough tracking distance radius in meters without needing a separate power-hungry GPS module.
*   **Twisting a dial for range control:** The board code checks a real physical potentiometer dial. If your friend is nearby, you can twist it down to low power (like +2 dBm) to save battery. If they're far away, you crank it to full power (+22 dBm) to push the message through concrete walls.

---

## master bill of materials (BOM)

### core computers & radios
*   Raspberry Pi 4 Model B (4GB RAM) | Robocraze | ₹9,599 each
*   SanDisk 64GB Micro SD-SDHC Memory Card | Robocraze | ₹1,889
*   HDMI to Micro HDMI Cable | Robocraze | ₹165
*   Waveshare SX1262 LoRa HAT for Raspberry Pi | Electro piiee | ₹7,076 (3 units @ ₹1,999 each including shipping)

### audio peripherals & visual displays
*   INMP441 MEMS Digital Microphone Module (I2S) | Robocraze | ₹360 (2 units @ ₹180 each)
*   SmartElex I2S Audio Breakout - MAX98357A | Techtonics | ₹480 (2 units @ ₹240 each)
*   3W 4-Ohm 2-Inch Full Range Stereo Audio Speaker Woofer | Robu.in | ₹240 (2 units @ ₹120 each)
*   0.96-inch SSD1306 OLED Display Module (4-Pin I2C) | Robu.in | ₹440 (2 units @ ₹220 each)

### portable power banks & hardware bits
*   Nextech 15W / 10000mAh CASE 3 Charging Power Bank | Robocraze | ₹1,400 (2 units @ ₹700 each)
*   400-Point Solderless Prototyping Breadboard | Robocraze | ₹150 (2 units @ ₹75 each)
*   12mm Momentary Tactile Push Buttons (5-Pack) | Robocraze | ₹60 (2 packs @ ₹20 each)
*   Male-to-Male (M-M) Jumper Wires Bundle | Robocraze | ₹150 (2 packs @ ₹70 each)
*   Female-to-Male (F-M) Jumper Wires Bundle | Robocraze | ₹150 (2 packs @ ₹70 each)
*   10k Ohm Metal Film Resistors (Pack of 10) | Robocraze | ₹25
*   Short USB-A to USB-C Data Cable | Robocraze | ₹120 (2 units @ ₹60 each)
*   LoRa Antenna 868MHz 3.2dBi SMA Male | Local | ₹300 (3 units @ ₹100 each)

### fabrication tools & case build setup
*   Noel 25W Soldering Iron Tool | Robocraze | ₹126
*   High-Grade Solder Wire Spool (90g) | Robocraze | ₹269
*   PerfBoad | Robocraz | ₹100 (Batch of 5-10 boards)
*   Sender Station Handheld Unit Case Setup (PETG frame, TPU bumpers, brass inserts, screws): ₹1,180
*   Receiver Station Handheld Unit Case Setup : ₹1,180

** total project cost:** ₹29,662 INR (about \$320.60 USD)
