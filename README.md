# ML-Based Keylogger Detection System

This project detects keylogger behavior using machine learning by analyzing
network traffic patterns instead of capturing keystrokes.

## Features
- Random Forest ML model
- Real-time detection
- Fedora & Windows compatible
- Multi-level alerts (Warning / Danger)
- Desktop notifications
- Safe attack simulator
- Log-based evidence

## How it Works
1. Collects short-window network statistics
2. Extracts behavioral features
3. Scales features using trained scaler
4. Predicts malicious probability
5. Alerts user if thresholds are crossed

## Ethical Note
A simulated keylogger is used for testing to avoid capturing real keystrokes.

## Run (Linux / Fedora)
```bash
pip install -r requirements.txt
python3 live_detector.py
