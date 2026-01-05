import time
import socket
import psutil
import requests
import subprocess

SERVER_URL = "http://127.0.0.1:8000/ingest"
API_KEY = "dev-key-change-me"
INTERVAL_SECONDS = 10
PING_TARGET = "1.1.1.1"  # change to your gateway or a key server

def get_disk_pct():
    return psutil.disk_usage("/").percent

def get_mem_pct():
    return psutil.virtual_memory().percent

def get_cpu_pct():
    return psutil.cpu_percent(interval=1)

def get_net_kbps(prev):
    counters = psutil.net_io_counters()
    now = (counters.bytes_recv, counters.bytes_sent, time.time())
    if prev is None:
        return 0.0, 0.0, now
    dt = max(0.001, now[2] - prev[2])
    rx_kbps = ((now[0] - prev[0]) * 8) / 1000.0 / dt
    tx_kbps = ((now[1] - prev[1]) * 8) / 1000.0 / dt
    return max(0.0, rx_kbps), max(0.0, tx_kbps), now

def ping_ms(target):
    try:
        # one ping; parse time=XX ms
        out = subprocess.check_output(["ping", "-c", "1", "-W", "1", target], text=True)
        for part in out.split():
            if part.startswith("time="):
                return float(part.split("=")[1])
    except Exception:
        return None
    return None

def main():
    host = socket.gethostname()
    prev = None
    while True:
        cpu = get_cpu_pct()
        mem = get_mem_pct()
        disk = get_disk_pct()
        rx, tx, prev = get_net_kbps(prev)
        p = ping_ms(PING_TARGET)

        payload = {
            "host": host,
            "cpu_pct": cpu,
            "mem_pct": mem,
            "disk_pct": disk,
            "rx_kbps": rx,
            "tx_kbps": tx,
            "ping_ms": p
        }

        try:
            r = requests.post(
                SERVER_URL,
                json=payload,
                headers={"X-API-Key": API_KEY},
                timeout=5
            )
            print("sent", r.status_code, payload)
        except Exception as e:
            print("send failed:", e)

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
