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

## Master Bill of Materials and Store Links

To construct both matching terminals, purchase these exact component choices from local Indian electronics distributors:

### Core Computers and Long-Range Radios (2 Pairs Needed)
* 2x Raspberry Pi 4 Model B (4GB RAM): [Robocraze Raspberry Pi 4 (4GB)](https://robocraze.com) - Main system host and message database server.
* 2x ESP32-S3 Development Board: [Robocraze ESP32-S3 Module](https://robocraze.com) - High-speed interface co-processor for audio and menus.
* 2x Waveshare SX1262 LoRa HAT for Raspberry Pi: [Robu.in Waveshare SX1262 Radio HAT](https://robu.in) - Long-range radio link transceiver.

### Audio Peripherals and Visual Displays (2 Pairs Needed)
* 2x INMP441 MEMS Digital Microphone Module (I2S): [Robocraze INMP441 Microphone (I2S)](https://robocraze.com) - High-precision omnidirectional digital audio input.
* 2x SmartElex I2S Audio Breakout - MAX98357A: [Techtonics MAX98357A Amplifier](https://techtonics.in) - Decodes digital frames directly for local audio output.
* 2x 3W 4-Ohm 2-Inch Full Range Stereo Audio Speaker Woofer: [Robu.in Audio Component Catalog](https://robu.in) - Dynamic sound cone designed for voice clarity.
* 2x 0.96-inch SSD1306 OLED Display Module (4-Pin I2C): [Robu.in 0.96-inch I2C OLED Panel](https://robu.in) - Screen interface used for menu systems and visual typing feedback.

### Portable Power Banks and Interconnects
* 2x Nextech 15W / 10000mAh CASE 3 Charging Power Bank: [Robocraze Power Supplies Search](https://robocraze.com) - Main portable power storage to run the nodes outside.
* 2x 400-Point Solderless Prototyping Breadboard: [Robocraze 400-Points Breadboard](https://robocraze.com) - Base for prototyping the handset circuits without soldering.
* 2x 12mm Momentary Tactile Push Buttons (5-Pack): [Robocraze Tactile Switches](https://robocraze.com) - Hardware keys for character entry, backspacing, and menu escaping.
* 2x Male-to-Male (M-M) Jumper Wires Bundle: [Robocraze M-M Jumper Cable Wires](https://robocraze.com) - Connects modules within the breadboard grid columns.
* 2x Female-to-Male (F-M) Jumper Wires Bundle: [Robocraze F-M Jumper Cable Wires](https://robocraze.com) - Connects the Raspberry Pi GPIO headers directly onto the breadboard rails.
* 1x 10k Ohm Metal Film Resistors (Pack of 10): [Robocraze 10k Ohm Resistors](https://robocraze.com) - Pull-up references for stable button operations.
* 2x Short USB-A to USB-C Data Cable: [Robocraze Type-C USB Interconnect Cable](https://robocraze.com) - Serial connection link between the Pi 4 and the ESP32.

---

## Hardware Wiring and Connections

This section details how to connect the external components to the ESP32-S3 board.

### Master Pin Interconnect Table

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
| **SSD1306 OLED Screen** | VCC | 3.3V | Logic Power |
| | GND | GND | Common System Ground |
| | SCL | GPIO 9 | I2C Hardware Clock Line |
| | SDA | GPIO 8 | I2C Hardware Data Line |
| **Button 1 (Type/Send)** | Terminal 1 | GPIO 1 | Input Signal Line (With 10k Resistor pull-up to 3.3V) |
| | Terminal 2 | GND | Short click: cycle letters / Long press: send message |
| **Button 2 (Backspace)** | Terminal 1 | GPIO 2 | Input Signal Line (With 10k Resistor pull-up to 3.3V) |
| | Terminal 2 | GND | Short click: delete last character |
| **Button 3 (Exit)**      | Terminal 1 | GPIO 42 | Input Signal Line (With 10k Resistor pull-up to 3.3V) |
| | Terminal 2 | GND | Short click: erase draft and exit menu |

### Physical Speaker Hookup
The raw connection leads extending from your 3W 4-Ohm 2-Inch Full Range Woofer screw directly into the positive (+) and negative (-) output block ports on the SmartElex MAX98357A module. Do not link these speaker wires directly into your breadboard holes.

---

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
