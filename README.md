
#  Off-Grid Radio Network for emergencies 
#  Made by meee Vaibhavv 
yo guyss before you read this I am vaibhav and i am a 9th grader and i have tried to make a innovation and help my country who is suffring from the problems and i have tried to make it fine as possible and also to help my future welll enjoy readingg!!

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
*   **6-minute power saver mode:** If you don't click any buttons for 6 minutes the ESP32 automatically cuts off power to the OLED screen panel . This keeps it from killing your battery, leaving only the LoRa chip listening quietly for incoming signals.so it lasts longgg
**   **Twisting a dial for range control:** The board code checks a real physical potentiometer dial. If your friend is nearby, you can twist it down to low power (like +2 dBm) to save battery. If they're far away, you crank it to full power  to push the message through concrete walls.

---

## master bill of materials (BOM)

* raspberry pi 3b	robocraze	₹4,790 / $57.02	1	₹4,790 / $57.02
* sandisk 32gb high-endurance micro sd	amazon	₹550 / $6.54	1	₹550 / $6.54
* waveshare sx1262 lora hat	robu.in	₹2,450 / $29.16	1	₹2,450 / $29.16
* lora antenna 868MHz 3.2dBi sma male	shokitech	₹280 / $3.33	3	₹840 / $10.00
* 5v 3a micro-usb power supply	robocraze	₹480 / $5.71	1	₹480 / $5.7
* custom 4-layer bare pcbs	pcbway	₹560 / $6.66	5	₹2,800 / $33.33
* esp32-s3fh4r2 microcontroller	lcsc	₹250 / $2.98	5	₹1,250 / $14.88
* ht-ct62 lora ic	lcsc	₹500 / $5.95	5	₹2,500 / $29.76
* icm-20948 9-axis imu	mouser	₹640 / $7.61	5	₹3,200 / $38.09power and audio ics + passives kit	lcsc	₹420 / $5.00	5	₹2,100 / $25.00
* dedicated ic for gps tracking	robu.in	₹620 / $7.38	2	₹1,240 / $14.76
* 3.7v 2000mAh lipo battery	robu.in	₹475 / $5.65	2	₹950 / $11.30
* 3w 4-ohm 2-inch speaker	robu.in	₹190 / $2.26	2	₹380 / $4.52
* 0.96-inch oled display (i2c)	robocraze	₹325 / $3.86	2	₹650 / $7.73
* u.fl to sma pigtail cable	robocraze	₹150 / $1.78	2	₹300 / $3.57
* 6x6x5mm push buttons (10-pack)	robocraze	₹50 / $0.59	1	₹50 / $0.59
* 3d printed cases (server + 2 handhelds)	pcbway 3d	₹1,200 / $14.28	3	₹3,600 / $42.85
* short usb-a to usb-c cable	robocraze	₹150 / $1.78	2	₹300 / $3.57
* pin headers and jumper wires	robocraze	₹200 / $2.38	1	₹200 / $2.38
* usb microsd reader	amazon	₹150 / $1.78	1	₹150 / $1.78
* 25w soldering iron and flux wire	robocraze	₹550 / $6.54	1	₹550 / $6.54
## Total cost of all off the componnets areee around ₹29,330 / $349.16
** YOoo guys remember the pricee of items are fluctuation so check twicee!!!

