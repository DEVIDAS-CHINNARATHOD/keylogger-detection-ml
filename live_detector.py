import time
import joblib
import subprocess
import pandas as pd
from datetime import datetime
from collector.network_stats import NetworkCollector

MODEL_PATH = "model/keylogger_rf.pkl"
SCALER_PATH = "model/scaler.pkl"
LOG_PATH = "logs/detections.log"

WARNING_THRESHOLD = 0.35
DANGER_THRESHOLD = 0.51

WARNING_HITS_REQUIRED = 2
DANGER_HITS_REQUIRED = 3

warning_hits = 0
danger_hits = 0

FEATURE_COLUMNS = [
    "packets_per_sec",
    "bytes_per_sec",
    "flow_duration",
    "fwd_packets",
    "fwd_bytes",
    "bwd_bytes",
    "process_activity_proxy",
    "bwd_subflow_packets",
    "active_time_mean"
]

def send_notification(title, message):
    subprocess.run(
        ["notify-send", title, message, "-u", "critical"],
        check=False
    )

def main():
    global warning_hits, danger_hits

    print("[*] Loading model and scaler...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    collector = NetworkCollector()

    print("[*] Keylogger detector started")
    print(f"[*] Warning threshold: {WARNING_THRESHOLD}")
    print(f"[*] Danger threshold: {DANGER_THRESHOLD}")

    while True:
        features = collector.collect()

        X = pd.DataFrame([features], columns=FEATURE_COLUMNS)
        X_scaled = scaler.transform(X)

        prob = model.predict_proba(X_scaled)[0][1]

        print(f"[{datetime.now()}] Keylogger probability: {prob:.3f}")

        # WARNING logic
        if WARNING_THRESHOLD <= prob < DANGER_THRESHOLD:
            warning_hits += 1
            danger_hits = 0
        else:
            warning_hits = 0

        # DANGER logic
        if prob >= DANGER_THRESHOLD:
            danger_hits += 1
        else:
            danger_hits = 0

        # Trigger WARNING
        if warning_hits >= WARNING_HITS_REQUIRED:
            send_notification(
                "Suspicious Activity Detected",
                f"Unusual network behavior (prob={prob:.2f})"
            )
            warning_hits = 0

        # Trigger DANGER
        if danger_hits >= DANGER_HITS_REQUIRED:
            msg = f"KEYLOGGER DETECTED (prob={prob:.2f})"

            send_notification(
                "KEYLOGGER DETECTED",
                msg
            )

            with open(LOG_PATH, "a") as log:
                log.write(f"{datetime.now()} | {msg}\n")

            danger_hits = 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Detector stopped safely")
