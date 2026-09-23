# Off-Grid Portable Multimedia Radio Network

A completely private, offline, and portable text-and-voice communication network designed to send messages between two identical stations over a local wide-area footprint. This system runs entirely on Sub-GHz radio waves without relying on Wi-Fi, internet routing infrastructure, or mobile cellular SIM cards.

## Purpose and Learning Goals
I am a high school student using this project to learn the fundamentals of decentralized hardware engineering, embedded systems, and wireless communications. Through this build, I am actively learning how to:
* Route real-time digital audio signals using the I2S protocol on an ESP32-S3 co-processor.
* Manage local text logging and serialization frameworks using a Raspberry Pi 4 Linux host server.
* Program Sub-GHz LoRa radio hardware to transmit long-range data packets.
* Design a custom 3-button keyboard and interface menu layout to cycle through characters on a portable OLED display without needing external desktop accessories.

---

## System Architecture and Hardware Division
The network consists of two completely duplicate, battery-powered stations (one sender and one receiver terminal). Each station uses a modular layout that balances fast, time-critical audio hardware routines with heavy file serialization:

### Roles of Each Board:
1. The Raspberry Pi 4: Runs the main operating system host, manages background chat logs, hosts a localized SQLite message database, and drives the Waveshare LoRa HAT to handle wide-area broadcasting.
2. The ESP32-S3: Acts as the dedicated frontend user interface. It captures 24-bit audio streams from the digital microphone, outputs sound through the Class-D amplifier, renders character layout frames to the OLED screen, and tracks individual hardware button presses.

---

## Bill of Materials (BOM)

This Bill of Materials details the components and tooling required to build one full operational pair (1 Sender Handset and 1 Base Receiver Station, totaling 2 physical nodes). 

### Core Computers & Radios
* **1x Raspberry Pi 4 Model B (4GB RAM)** | Supplier: Robocraze | Price: ₹9,599 each
* **1x SanDisk 64GB Micro SD-SDHC Memory Card** | Supplier: Robocraze | Price: ₹1,889
* **1x HDMI to Micro HDMI Cable** | Supplier: Robocraze | Price: ₹165
* **2x ESP32-S3 Development Board** | Supplier: Robocraze | Price: ₹1,798 (₹899 each)
* **3x Waveshare SX1262 LoRa HAT for Raspberry Pi** | Supplier: Electro piiee | Price: ₹7,076 (₹1,999 each including shipping)

### Audio Peripherals & Visual Displays
* **2x INMP441 MEMS Digital Microphone Module (I2S)** | Supplier: Robocraze | Price: ₹360 (₹180 each)
* **2x SmartElex I2S Audio Breakout - MAX98357A** | Supplier: Techtonics | Price: ₹480 (₹240 each)
* **2x 3W 4-Ohm 2-Inch Full Range Stereo Audio Speaker Woofer** | Supplier: Robu.in | Price: ₹240 (₹120 each)
* **2x 0.96-inch SSD1306 OLED Display Module (4-Pin I2C)** | Supplier: Robu.in | Price: ₹440 (₹220 each)

### Portable Power Banks & Interconnects
* **2x Nextech 15W / 10000mAh CASE 3 Charging Power Bank** | Supplier: Robocraze | Price: ₹1,400 (₹700 each)
* **2x 400-Point Solderless Prototyping Breadboard** | Supplier: Robocraze | Price: ₹150 (₹75 each)
* **2x 12mm Momentary Tactile Push Buttons (5-Pack)** | Supplier: Robocraze | Price: ₹60 (₹20 each)
* **2x Male-to-Male (M-M) Jumper Wires Bundle** | Supplier: Robocraze | Price: ₹150 (₹70 each)
* **2x Female-to-Male (F-M) Jumper Wires Bundle** | Supplier: Robocraze | Price: ₹150 (₹70 each)
* **1x 10k Ohm Metal Film Resistors (Pack of 10)** | Supplier: Robocraze | Price: ₹25
* **2x Short USB-A to USB-C Data Cable** | Supplier: Robocraze | Price: ₹120 (₹60 each)

### Fabrication Tools & Manufacturing Services
* **1x Noel 25W Soldering Iron Tool** | Supplier: Robocraze | Price: ₹126
* **1x High-Grade Solder Wire Spool (90g)** | Supplier: Robocraze | Price: ₹269
* **1x Custom Printed Circuit Board Manufacturing Run** | Supplier: PCBWay | Price: ₹2,100 (Covers a custom batch run of 5-10 bare prototype boards)
* **3x LoRa Antenna 868MHz 3.2dBi SMA Male** | Supplier: Local | Price: ₹300 (₹100 each)

### Custom Protective Enclosures
We migrated from baseline 3D plastic shells to a high-durability, multi-material modular structural layout (Rigid PETG Core + Shock-absorbing TPU bumpers/seals).

#### 1. Sender Handset Enclosure
* **Rigid PETG Core Frame, Rear Battery Clip & Buttons** (120g @ ₹6/g): ₹720
* **Flexible TPU Shock Bumpers, Dust Plugs & Seals** (35g @ ₹8/g): ₹280
* **Hardware Pack** (4x Brass Inserts, 4x M3 Thumbscrews, O-ring cord, Acrylic tape): ₹180
* *Sender Case Subtotal:* ₹1,180 INR

#### 2. Receiver Base Enclosure
* **Rigid PETG Core Frame, Rear Battery Clip & Buttons** (120g @ ₹6/g): ₹720
* **Flexible TPU Shock Bumpers, Dust Plugs & Seals** (35g @ ₹8/g): ₹280
* **Hardware Pack** (4x Brass Inserts, 4x M3 Thumbscrews, O-ring cord, Acrylic tape): ₹180
* *Receiver Case Subtotal:* ₹1,180 INR

---

### Project Financial Summary
* **Estimated Project Grand Total:** **₹31,662 INR** (~$330.73 USD)

> *Note on Sourcing:* Utilizing local Indian engineering distribution channels (Robocraze, Robu.in, Techtonics) helps minimize global logistics delays, keeps component pathways fully trackable, and completely bypasses high international clearing fees to expedite development milestones.


---

## Hardware Wiring and Connections

This section details how to connect the external components to the ESP32-S3 board.

### Master Pin Interconnect Table

## Master Hardware Wiring and Pin Mapping Guides

The system uses a 3-Node Relay Architecture comprising two identical handheld terminals (Node A: Sender, Node B: Receiver) and a central routing hub (Node C: Home Base Server). 

### Handheld Unit Configurations (Node A and Node B)

All peripheral modules route directly into the custom PCB traces mapped to the ESP32-S3 pins as follows:

| Module Peripheral | Module Pin Name | Target Pin (ESP32-S3) | Circuit Wire Function |
| :--- | :--- | :--- | :--- |
| **INMP441 Microphone** | VCC | 3.3V | Logic Power |
| | GND | GND | Common System Ground |
| | SD | GPIO 13 | I2S Data Input Stream |
| | WS | GPIO 14 | I2S Left/Right Clock |
| | SCK | GPIO 12 | I2S Serial Bit Clock |
| | L/R | GND | Set to Left Input Channel |
| **SmartElex MAX98357A**| VIN | 5V / VBUS | 5V Power for Speaker Amp |
| | GND | GND | Common System Ground |
| | DIN | GPIO 21 | I2S Data Output Stream |
| | LRC | GPIO 47 | I2S Word Selection Clock |
| | BCLK | GPIO 48 | I2S Serial Bit Clock |
| **Waveshare SX1262 LoRa**| VCC | 3.3V | Radio Logic Power |
| | GND | GND | Common System Ground |
| | MOSI | GPIO 11 | SPI Master Output Slave Input |
| | MISO | GPIO 13 | SPI Master Input Slave Output |
| | SCK | GPIO 12 | SPI Serial Clock Line |
| | NSS / CS | GPIO 10 | SPI Chip Select |
| | DIO1 | GPIO 5 | Digital Interrupt Output 1 |
| | BUSY | GPIO 6 | Radio Busy Status Indicator |
| | RST | GPIO 7 | Radio Hardware Reset Line |
| **SSD1306 OLED Screen** | VCC | 3.3V | Logic Power |
| | GND | GND | Common System Ground |
| | SCL | GPIO 9 | I2C Hardware Clock Line |
| | SDA | GPIO 8 | I2C Hardware Data Line |
| **Button 1 (Type/Send)** | Terminal 1 | GPIO 1 | Input Signal Line (With 10k Resistor pull-up to 3.3V) |
| | Terminal 2 | GND | Short click: cycle letters / Long press: send message |
| **Button 2 (Backspace)** | Terminal 1 | GPIO 2 | Input Signal Line (With 10k Resistor pull-up to 3.3V) |
| | Terminal 2 | GND | Short click: delete last character / Cycle forward when draft empty |
| **Button 3 (Exit)**      | Terminal 1 | GPIO 42 | Input Signal Line (With 10k Resistor pull-up to 3.3V) |
| | Terminal 2 | GND | Short click: erase draft and exit menu |

### Physical Handheld Speaker Hookup
The raw connection leads extending from your 3W 4-Ohm 2-Inch Full Range Woofer screw directly into the positive (+) and negative (-) output block ports on the SmartElex MAX98357A module. Do not link these speaker wires directly into your PCB header pin holes or breadboard rails.

---

### Home Base Station Configuration (Node C)

The home relay server mounts the standard transceiver stack directly onto the main operating system host headers:

| Module Peripheral | Module Pin Name | Target Pin (Raspberry Pi 4) | Circuit Wire Function |
| :--- | :--- | :--- | :--- |
| **Waveshare SX1262 HAT**| 5V | Physical Pin 2 / 4 | Main Hardware System Power |
| | GND | Physical Pin 6 / 9 / 14 | Common System Ground |
| | MOSI | Pin 19 / GPIO 10 | SPI0 Master Output Slave Input |
| | MISO | Pin 21 / GPIO 9 | SPI0 Master Input Slave Output |
| | SCLK | Pin 23 / GPIO 11 | SPI0 Serial Clock Line |
| | CE0 | Pin 24 / GPIO 8 | SPI0 Chip Select Line |
| | RST | Pin 22 / GPIO 25 | Radio Hardware Reset Line |
| | BUSY | Pin 18 / GPIO 24 | Radio Busy Status Indicator |
| | DIO1 | Pin 16 / GPIO 23 | Digital Interrupt Output 1 |

### Home Base Station Power Hookup
The Raspberry Pi 4 Base Hub remains continuously active as the central database relay and operates via its dedicated on-board USB-C power inlet driven by a standard multi-amperage mains power supply or dedicated high-capacity backup array.


## Custom 3-Button Typing Interface C++ Code

This production code runs on the ESP32-S3 co-processor. It handles your 3-button menu navigation array, renders dynamic text updates onto the OLED screen, and tracks button hold states to trigger message transmission.

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define I2C_SDA        8
#define I2C_SCL        9
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Target Input Pin Declarations
#define BUTTON_TYPING      1
#define BUTTON_BACKSPACE   2
#define BUTTON_EXIT       42

// Typing Menu Storage Frameworks
const char alphabet[] = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.!?";
int alphabet_index = 0;
String current_draft = "";
bool menu_active = true;

void setup() {
  Serial.begin(115200);
  
  // Set up button pins as input pull-ups
  pinMode(BUTTON_TYPING, INPUT_PULLUP);
  pinMode(BUTTON_BACKSPACE, INPUT_PULLUP);
  pinMode(BUTTON_EXIT, INPUT_PULLUP);
  
  // Start I2C bus and screen
  Wire.begin(I2C_SDA, I2C_SCL);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED allocation failed");
    for(;;);
  }
  
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  updateDisplayView();
}

void updateDisplayView() {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("--- OFFLINE TEXT MENU ---");
  
  // Render current message string draft
  display.setCursor(0, 16);
  display.print("Msg: ");
  display.println(current_draft);
  
  // Render active selection loop index character
  display.setCursor(0, 40);
  display.print("Select Character: [ ");
  display.print(alphabet[alphabet_index]);
  display.println(" ]");
  
  display.setCursor(0, 54);
  display.println("[Hold Type Button To Send]");
  display.display();
}

void triggerMessageSend() {
  display.clearDisplay();
  display.setCursor(0, 20);
  display.println(">> PACKET SENDING...");
  display.print("Payload: ");
  display.println(current_draft);
  display.display();
  
  // Output message data down the UART Serial data link line to the Pi 4
  Serial.println("TX_DATA:" + current_draft);
  
  delay(1500); 
  current_draft = ""; // Reset internal memory storage string
  alphabet_index = 0;
  updateDisplayView();
}

void loop() {
  if (!menu_active) return;

  // 1. Manage Button 1: Typing and Send Actions
  if (digitalRead(BUTTON_TYPING) == LOW) {
    delay(50); // Software debounce
    unsigned long press_start = millis();
    bool long_press_detected = false;
    
    // Hold evaluation block loop
    while (digitalRead(BUTTON_TYPING) == LOW) {
      if (millis() - press_start > 2500) { // 2.5 second intentional hold threshold
        long_press_detected = true;
        break;
      }
    }
    
    if (long_press_detected) {
      if (current_draft.length() > 0) {
        triggerMessageSend();
      }
    } else {
      // Short click adds character to your draft string layout
      current_draft += alphabet[alphabet_index];
      alphabet_index = 0; // Reset focus letter back to start space
      updateDisplayView();
    }
    while(digitalRead(BUTTON_TYPING) == LOW); // Wait for physical release
  }

  // 2. Manage Button 2: Character Backspacing Loop
  if (digitalRead(BUTTON_BACKSPACE) == LOW) {
    delay(150); // Debounce interval
    
    // Cycle the character under selection forward if tapped quickly
    if (current_draft.length() == 0) {
      alphabet_index++;
      if (alphabet_index >= sizeof(alphabet) - 1) alphabet_index = 0;
    } else {
      // Backspace clears text character history strings
      current_draft.remove(current_draft.length() - 1);
    }
    updateDisplayView();
    while(digitalRead(BUTTON_BACKSPACE) == LOW);
  }

  // 3. Manage Button 3: Wiping Data and Exiting Out
  if (digitalRead(BUTTON_EXIT) == LOW) {
    delay(200);
    current_draft = "";
    alphabet_index = 0;
    
    display.clearDisplay();
    display.setCursor(0, 20);
    display.println("Menu Cleared. Idle RX Mode.");
    display.display();
    
    while(digitalRead(BUTTON_EXIT) == LOW);
    delay(1000);
    updateDisplayView();
  }
}
```
