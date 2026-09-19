# 
| Peripheral | Pin Name | Target Pin (ESP32-S3) | Description |
| :--- | :--- | :--- | :--- |
| **INMP441 Microphone** | VCC | 3.3V | 3.3V Power Supply |
| | GND | GND | Ground |
| | SD | GPIO 13 | I2S Data Input |
| | WS | GPIO 14 | I2S Word Select |
| | SCK | GPIO 12 | I2S Clock |
| | L/R | GND | Select Left Channel |
| **MAX98357A Amplifier** | VIN | 5V / VBUS | 5V Power Supply |
| | GND | GND | Ground |
| | DIN | GPIO 21 | I2S Data Output |
| | LRC | GPIO 47 | I2S Word Select |
| | BCLK | GPIO 48 | I2S Clock |
| **SSD1306 OLED Screen** | VCC | 3.3V | 3.3V Power Supply |
| | GND | GND | Ground |
| | SCL | GPIO 9 | I2C Clock |
| | SDA | GPIO 8 | I2C Data |
| **Push-to-Talk Button** | Pin 1 | GPIO 1 | Connect to 10k resistor pull-up to 3.3V |
| | Pin 2 | GND | Connects to Ground on press |
| **Menu Button** | Pin 1 | GPIO 2 | Connect to 10k resistor pull-up to 3.3V |
| | Pin 2 | GND | Connects to Ground on press |




 # Off-Grid Neighborhood Multimedia Radio Grid

A private, completely offline walkie-talkie and text mesh network designed to communicate between two identical stations over a local wide area network. This system operates entirely on raw radio waves without relying on Wi-Fi, internet routing infrastructure, or mobile cellular SIM cards.

## Purpose & Learning Goals
I am a school student using this project to learn how microcontrollers and single-board computers work together in real-world setups. Through this build, I am learning:
* How to route high-speed digital audio signals over the I2S protocol using an ESP32-S3.
* How to log and serialize local text communications into a database running on a Raspberry Pi 4 Linux server.
* How to transmit data packets across a neighborhood using Sub-GHz peer-to-peer LoRa radio modules.

---

## Complete Project Budget & Purchase Links

To build both sides of the network (one sender and one receiver), the following matching parts are required from local Indian electronics distributors:

### 1. Main Processing Core (2 Units Required)
* **Raspberry Pi 4 Model B (4GB RAM):** [Robocraze Raspberry Pi 4 (4GB)](https://robocraze.com) - Main system host and message database server.
* **ESP32-S3 Development Board:** [Robocraze ESP32-S3 Module](https://robocraze.com) - Hardware co-processor for audio and menus.

### 2. Radio & Audio Interfacing (2 Units Required)
* **Waveshare Core1262-HF LoRa Module (SX1262):** [Robocraze Waveshare SX1262 Radio](https://robocraze.com) - Long-range radio link.
* **INMP441 MEMS Digital Microphone Module (I2S):** [Robocraze INMP441 Microphone (I2S)](https://robocraze.com) - Crisp digital audio voice input.
* **MAX98357A I2S Class-D Audio Amplifier Module:** [Techtonics MAX98357A Amplifier](https://techtonics.in) - Decodes audio frames for playback.
* **Small 8-Ohm 3W Dynamic Speaker:** [Robu.in Audio Component Catalog](https://robu.in) - Physical audio output.

### 3. Displays, Hardware Controls & Wiring Supplies
* **0.96-inch SSD1306 OLED Display Module (4-Pin I2C):** [Robu.in 0.96-inch I2C OLED Panel](https://robu.in) - Handset interface display menus.
* **12mm Momentary Tactile Push Buttons (5-Pack):** [Robocraze Tactile Switches](https://robocraze.com) - Push-to-Talk and option navigation buttons.
* **400-Point Solderless Prototyping Breadboard:** [Robocraze 400-Points Breadboard](https://robocraze.com) - Holds temporary prototype circuits securely.
* **Male-to-Male (M-M) Jumper Wires Bundle:** [Robocraze M-M Jumper Cable Wires](https://robocraze.com) - Connects modules inside the breadboard grid.
* **Female-to-Male (F-M) Jumper Wires Bundle:** [Robocraze F-M Jumper Cable Wires](https://robocraze.com) - Links the Raspberry Pi pins over to the breadboard.
* **10k Ohm Metal Film Resistors (Pack of 10):** [Robocraze 10k Ohm Resistors](https://robocraze.com) - Pull-down references for clean button signals.
* **Short USB-A to USB-C Data Cable:** [Robocraze Type-C USB Interconnect Cable](https://robocraze.com) - Bridges the data link between the Pi 4 and the ESP32.

---
