from datetime import datetime
import os
import re
import sqlite3

VOICE_DIR = "voice_vault"
os.makedirs(VOICE_DIR, exist_ok=True)  # Native clean directory creation


def _db_exec(query, params):
    # Shared minimal helper to strip connection boilerplate
    with sqlite3.connect("offgrid_network.db") as conn:
        conn.execute(query, params)


def parse_incoming_radio_frame(raw_frame, rssi, snr):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. System Initialization Frame
    if "[SYS_INIT]" in raw_frame:
        m = re.search(r"\[SRC:([^\]]+)\]", raw_frame)
        s_id = m.group(1) if m else "UNKNOWN"
        _db_exec(
            "INSERT OR REPLACE INTO tracked_peers VALUES (?, ?, 'ONLINE', ?, ?, ?)",
            (s_id, f"ESP32 Node #{s_id}", ts, rssi, snr),
        )
        print(f"\n📡 [ping] node {s_id} checked in. signal: {rssi} dBm")

    # 2. Text Message Cache Frame
    elif "[DST:" in raw_frame and "[V_NOTE:" not in raw_frame:
        m = re.search(r"\[SRC:([^\]]+)\].*?\[DST:([^\]]+)\](.*)", raw_frame)
        if not m:
            return print(f"bad string packet format: {raw_frame}")
        s, r, body = m.group(1), m.group(2), m.group(3).strip("] ")
        _db_exec(
            "INSERT INTO text_vault (timestamp, sender, receiver, message) VALUES (?, ?, ?, ?)",
            (ts, s, r, body),
        )
        print(f"\n📨 [text cached] {s} -> {r}: \"{body}\"")

    # 3. Voice Note Ledger Allocation
    elif "[V_NOTE:" in raw_frame:
        m = re.search(r"\[V_NOTE:#([^:]+):([^\]]+)\]", raw_frame)
        if not m:
            return print("voice header broke on the way, dropping")
        s, bytes_expected = m.group(1), int(m.group(2))
        f_path = os.path.join(VOICE_DIR, f"voice_{s}_{int(datetime.now().timestamp())}.raw")
        _db_exec(
            "INSERT INTO voice_ledger (timestamp, sender, file_size_bytes, file_path) VALUES (?, ?, ?, ?)",
            (ts, s, bytes_expected, f_path),
        )
        print(f"\n🎙️ [voice track open] sender: #{s} | size: {bytes_expected}b -> saving to /{f_path}")


if __name__ == "__main__":
    print("gateway debug loop active.")
