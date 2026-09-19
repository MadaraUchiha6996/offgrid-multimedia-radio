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
