\# Off-Grid Portable Multimedia Radio Network



An autonomous, decentralized, and encrypted peer-to-peer ad-hoc communication network designed to provide mission-critical text telemetry, location mapping, and ultra-compressed digital voice messaging during catastrophic disaster events when standard cell towers, Wi-Fi infrastructure, and internet links fail completely.



\##  System Architecture \& Directory Topology



```text

OffGridRadioServer/

│

├── packet.py             # Binary Protocol Layout (Header Structs)

├── services.py           # Discovery Beacon \& GPS Compressed Encoders

├── network\_env.py        # Asynchronous RF Air Interface Simulation

├── routing.py            # Mesh Router, Deduplication \& TTL Manager

├── audio\_codec.py        # Voice Note 10s Fragmentation/Assembly 

├── database.py           # Context-Managed Power-Failure Protected SQL Store

├── security.py           # Isolated Symmetric XOR Cipher (Dynamic Key Masking)

├── gateway.py            # Automated Hybrid Internet WAN Routing Bridge

├── satellite\_receiver.py # DVB-S Satellite Dish Downlink Demux Ingestion

├── main\_server.py        # Master Coordinator Server Loop Daemon

├── hardware\_lora.py      # Low-Level SPI/GPIO Waveshare Radio Interface Driver

└── offgrid\_radio.service # Linux systemd Boot Automation Configuration

```



\##  Custom Binary Protocol Specification



To maximize performance on constrained Sub-GHz LoRa channels, data frames utilize a strict, unpadded fixed 10-byte header layout packed in explicit little-endian format (`<`):



| Offset (Bytes) | Field Name    | Data Type | Description                                   |

|----------------|---------------|-----------|-----------------------------------------------|

| 0              | magic\_byte    | uint8\_t   | Protocol verification sequence (`0xA5`)       |

| 1              | version       | uint8\_t   | Framework iteration tracking indicator        |

| 2              | packet\_type   | uint8\_t   | Type identifier (TEXT, GPS, VOICE, REQ\_MSG)   |

| 3              | flags         | uint8\_t   | Bit 0: ACK Required \\| Bit 1: Encrypted Payload|

| 4-5            | source\_node   | uint16\_t  | Origin transmitter address coordinate ID      |

| 6-7            | dest\_node     | uint16\_t  | Destination target ID (`0xFFFF` = Broadcast)   |

| 8              | packet\_id     | uint8\_t   | Deduplication sequencing tracking index       |

| 9              | ttl           | uint8\_t   | Time To Live hop degradation boundary limit   |

| 10+            | payload       | bytes     | Raw data bytes payload boundary (Max 246B)    |



\##  Base Station Jumper Wire Pinout Mapping

Connections from the Raspberry Pi 4 BCM GPIO interfaces to the Waveshare SX1262 LoRa HAT:



\* \*\*MOSI\*\* -> GPIO 10 (Pin 19)

\* \*\*MISO\*\* -> GPIO 9 (Pin 21)

\* \*\*SCK\*\*  -> GPIO 11 (Pin 23)

\* \*\*NSS / CS\*\* -> GPIO 8 (Pin 24)

\* \*\*BUSY\*\* -> GPIO 24 (Pin 18)

\* \*\*RST\*\*  -> GPIO 22 (Pin 15)

\* \*\*DIO1\*\* -> GPIO 25 (Pin 22)



\## Production Deployment Reference Manual



\### 1. Verification

Execute the local simulation validation script block to verify file paths and package bindings run cleanly without syntax faults:

```bash

python main\_server.py

```



\### 2. Auto-Boot System Daemon Configuration

Configure the systemd service to automate script execution immediately upon hardware power attachment:

```bash

\# Copy system profile to daemon configuration paths

sudo cp offgrid\_radio.service /etc/systemd/system/



\# Reload structural index changes

sudo systemctl daemon-reload



\# Activate the initialization routine at boot sequence

sudo systemctl enable offgrid\_radio.service



\# Boot the active background daemon profile immediately

sudo systemctl start offgrid\_radio.service

```



