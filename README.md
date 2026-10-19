

#  Off-Grid Radio Network for emergencies 
#  Made by meee Vaibhavv 
yo guyss before you read this I am vaibhav and i am a 9th grader and i have tried to make a innovation and help my country who is suffring from the problems and i have tried to make it fine as possible and also to help my future welll enjoy readingg!!

So basically this project is an offline communication setup meant for disasters when standard internet and cell towers go completely dark. It uses a main home base station linked to small portable handheld walkie-talkie units. They talk over raw radio waves without needing any active sim cards, wifi, or external provider networks.

### how the system layout works

The whole thing splits into two main sections that connect automatically:
1. **The Handheld Walkie-Talkie (ESP32-S3):** This takes your voice notes through an I mic, shows details on a small OLED display screen, and lets you type out messages using a simple button menu. 
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

* raspberry pi 3b	robocraze	₹4,790 / $57.02	|1	₹4,790 / $57.02
* sandisk 32gb high-endurance micro sd	amazon	₹550 / $6.54	|1	₹550 / $6.54
* waveshare sx1262 lora hat	robu.in	₹2,450 / $29.16	|1	₹2,450 / $29.16
* lora antenna 868MHz 3.2dBi sma male	shokitech	₹280 / $3.33|3	₹840 / $10.00
* 5v 3a micro-usb power supply	robocraze	₹480 / $5.71	|1	₹480 / $5.7
* custom 4-layer bare pcbs	pcbway	₹560 / $6.66	|5	₹2,800 / $33.33
* esp32-s3fh4r2 microcontroller	lcsc	₹250 / $2.98	|5	₹1,250 / $14.88
* ht-ct62 lora ic	lcsc	₹500 / $5.95	5	₹2,500 / $29.76
* icm-20948 9-axis imu	mouser	₹640 / $7.61	5	₹3,200 / $38.09power and audio ics + passives kit	lcsc	₹420 / $5.00	5	₹2,100 / $25.00
* dedicated ic for gps tracking	robu.in	₹620 / $7.38	2	₹1,240 / $14.76
* 3.7v 2000mAh lipo battery	robu.in	₹475 / $5.65	2	₹950 / $11.30
* 3w 4-ohm 2-inch speaker	robu.in	₹190 / $2.26	2	₹380 / $4.52
* 0.96-inch oled display (i2c)	robocraze	₹325 / $3.86	2	₹650 / $7.73
* u.fl to sma pigtail cable	robocraze	₹150 / $1.78	2	₹300 / $3.57
* 6x6x5mm push buttons (10-pack)	robocraze	₹50 / $0.59	|1	₹50 / $0.59
* 3d printed cases (server + 2 handhelds)	pcbway 3d	₹1,200 / $14.28	|3	₹3,600 / $42.85
* short usb-a to usb-c cable	robocraze	₹150 / $1.78	|2	₹300 / $3.57
* pin headers and jumper wires	robocraze	₹200 / $2.38	|1	₹200 / $2.38
* usb microsd reader	amazon	₹150 / $1.78	|1	₹150 / $1.78
* 25w soldering iron and flux wire	robocraze	₹550 / $6.54	|1	₹550 / $6.54
## Total cost of all off the componnets areee around ₹29,330 / $349.16
** YOoo guys remember the pricee of items are fluctuation so check twicee!!!
<img width="959" height="539" alt="Screenshot 2026-10-09 204957" src="https://github.com/user-attachments/assets/6d1dc55e-cd33-4997-95b9-58a5277498d7" />
<img width="959" height="539" alt="Screenshot 2026-10-09 204859" src="https://github.com/user-attachments/assets/ded880c8-33e6-452a-83f4-dbd4cb3ccda0" />
## List of features for people wondering
* Gps
* Display
* in bulilt mic and speaker
* range upto 25 and 10km
* internet gate way
* uses no pre built
* Completely off grid
* uses mesh protocol
* power to send voice notes upto 10sec
* encryption
* can send text msg
* range control
* uses battery which can be rechargebale
* portable
* cost effective and cheap
* made total by a 9thgrader
* uses radio waves
* server backups
* total control over your device
* and many more

## Some explanation  on how it works 
*off grid multimedia radio

hi im vaibhav and this is my project, its basically a walkie talkie but with way more stuff in it than anyone puts in one device. you can send text and short voice msgs, see where u are on a little map, know which way is north, and it can even call for help if u fall down. and it all keeps working when the power is out and theres no internet why i made it, when theres a blackout or a big storm phones just die. normal walkie talkies still work but they dont go far and cant do anything smart. i wanted one thing that keeps going when everything else stops the main esp32 s3 does the processing work, like zipping the voice note and making the packets, and it also handles the gps and the gyroscope. the second one is an esp32 c3 with the ht-ct62 lora chip and it only handles the data transfer, sending and recieving. theres a high gain antina on it for range the server is a raspberry pi 3b with 1gb ram and it sits in ur home or anywhere u want. it gets the signal from the handheld and checks for bugs, broken msgs, missing packets etc, then it saves the msg and bounces it to the reciever. u can also request old msgs from it later i will be adding a small ai bot on the pi that helps u in emergencies, like if ur wounded and dont know how to cover the wound or what the dose of a medicine is, u can ask it. it has limits too so it cant do things it shouldnt, and it tells u to get real help when u can for gps theres a chip inside so it knows where u are. theres a simple map of ur area saved on the device, not like google maps, more like a drawing with roads and landmarks and a dot for u. theres a compass too. it keeps watching ur location, mic and gyroscope and if something weird happens like a sudden hit or fall it tells the server

features i have

gps tracking with a simple offline map
range around 10 km in open areas and upto 25 km if nothing is in the way, hills and buildings make it shorter
ai helper on the server that talks over the radio
text msgs and voice msgs upto 10 sec
mesh routing so handhelds can pass msgs along for more range
internet gateway as a backup
fully offline, made for blackouts
built in compass
request old msgs back from the server
auto connect, turn it on and it finds the nearest server by itself
encrypted msgs
every feature can be turned on and off
spam protection
0.96 inch oled and a keyboard tray that guesses ur next word
rechargeable battery around 2 days of use, no power bank needed
portable

it runs at 866.5 mhz which is inside the license free band in india (865 to 867 mhz) so no license is needed. still gotta double check the power limit in the rules before i finish

not gonna lie i havent proven everything yet. real range changes a lot depending on where u are so 25 km is the best case not the normal case. voice over lora is slow so voice msgs are short and squished a lot. battery life depends on how much gps and radio u use. and the helper bot is small cuz the pi 3b is small so its answers are simple

rough bom is ₹29,330 / $349.16 for 5 handhelds and 1 server. pcb is custom made in kicad and the schematic and pcb are in the journal md file in this repo

this helps me learn way more about robotics and engineering and i think it can actually help people too. readme will be updated more soon, any doubts then contact me on slack. thanks for reading and i hope u like it

