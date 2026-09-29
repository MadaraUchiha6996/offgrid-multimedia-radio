# Off-Grid Portable Multimedia Radio Network

An autonomous, decentralized, and encrypted peer-to-peer ad-hoc communication network designed for emergency communication.

## Project Description
Provides a zero-infrastructure communication link for localized emergencies by deploying localized RF transceivers, dividing tasks between a stationary base station hub and ultra-portable handheld field units.

## Core System Features
* **Zero-Infrastructure Connectivity:** Operates independently of cellular carriers or Wi-Fi.
* **Custom Binary Air Interface Protocol:** Utilizes an efficient header layout for Sub-GHz channels.
* **Text & Voice Support:** Supports alphanumeric broadcasting and digital audio streams.
* **Power-Failure Protected Storage:** Utilizes local database engines for asynchronous packet handling.

## Technical Component Role Breakdown
1. **Centralized Server Hub (Raspberry Pi 4 Model B):** Acts as primary coordinator, packet router, and database warehouse.
2. **Handheld Field Transceiver (ESP32-S3 Development Board):** Low-latency node handling user input, displays, and audio/radio streaming.
3. **Sub-GHz Radio Engine (Waveshare SX1262 LoRa HAT):** Handles physical layer RF modulation via SPI.

## Master Bill of Materials (BOM)
##Core Computers & Radios
* **• Raspberry Pi 4 Model B (4GB RAM) | Robocraze | ₹9,599 each**
* **• Raspberry Pi 4 Model B (4GB RAM) | Robocraze | ₹9,599 each**
* **• SanDisk 64GB Micro SD-SDHC Memory Card | Robocraze | ₹1,889**
* **• HDMI to Micro HDMI Cable | Robocraze | ₹165**
* * **• Waveshare SX1262 LoRa HAT for Raspberry Pi | Electro piiee | ₹7,076 (3 units @ ₹1,999 each including shipping)**
##Audio Peripherals & Visual Displays
* **• INMP441 MEMS Digital Microphone Module (I2S) | Robocraze | ₹360 (2 units @ ₹180 each)**
* **• SmartElex I2S Audio Breakout - MAX98357A | Techtonics | ₹480 (2 units @ ₹240 each)**
* **• 3W 4-Ohm 2-Inch Full Range Stereo Audio Speaker Woofer | Robu.in | ₹240 (2 units @ ₹120 each)**
* **• 0.96-inch SSD1306 OLED Display Module (4-Pin I2C) | Robu.in | ₹440 (2 units @ ₹220 each)**
##Portable Power Banks & Interconnects
* **• Nextech 15W / 10000mAh CASE 3 Charging Power Bank | Robocraze | ₹1,400 (2 units @ ₹700 each)**
* **• 400-Point Solderless Prototyping Breadboard | Robocraze | ₹150 (2 units @ ₹75 each)**
* **• 12mm Momentary Tactile Push Buttons (5-Pack) | Robocraze | ₹60 (2 packs @ ₹20 each)**
* **• Male-to-Male (M-M) Jumper Wires Bundle | Robocraze | ₹150 (2 packs @ ₹70 each)**
* **• Female-to-Male (F-M) Jumper Wires Bundle | Robocraze | ₹150 (2 packs @ ₹70 each)**
* **• 10k Ohm Metal Film Resistors (Pack of 10) | Robocraze | ₹25**
* **• Short USB-A to USB-C Data Cable | Robocraze | ₹120 (2 units @ ₹60 each)**
* **• LoRa Antenna 868MHz 3.2dBi SMA Male | Local | ₹300 (3 units @ ₹100 each)**
##Fabrication Tools & Manufacturing Services
* **• Noel 25W Soldering Iron Tool | Robocraze | ₹126**
* **• High-Grade Solder Wire Spool (90g) | Robocraze | ₹269**
* **• PerfBoad | Robocraz | ₹100 (Batch of 5-10 boards)**
##Custom Device Enclosure Cost Breakdown
* **• Sender Station Case (Handheld Unit) | ₹1,180**
* **• Rigid PETG Frame, Battery Clip, & Buttons (120g): ₹720**
* **• Flexible TPU Shock Bumpers, Dust Plugs, & Seals (35g): ₹280**
* **• Hardware Pack (Brass Inserts, M3 Thumbscrews, O-ring, Tape): ₹180**
* **Receiver Station Case (Handheld Unit) | ₹1,180**
* **• Rigid PETG Frame, Battery Clip, & Buttons (120g): ₹720**
* **• Flexible TPU Shock Bumpers, Dust Plugs, & Seals (35g): ₹280**
* **• Hardware Pack (Brass Inserts, M3 Thumbscrews, O-ring, Tape): ₹180**
* **Grand Total Project Cost**
* **₹31,662 INR (approx. $330.73 USD)**

## Infrastructure Hardware Wiring Pinout Guides
* **Server Unit (Raspberry Pi 4 to SX1262):** SPI bus connections, control signals (CS, Busy, Reset, DIO1), and power/ground rails.
* **Handheld Unit (ESP32-S3 to Peripherals):** Dedicated GPIO mappings for the LoRa module, OLED display, navigation buttons, INMP441 microphone, and MAX98357A amplifier.
