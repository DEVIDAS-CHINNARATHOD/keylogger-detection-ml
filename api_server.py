import joblib
import pandas as pd
from flask import Flask, request, jsonify
import os

MODEL_PATH = "model/keylogger_rf.pkl"
SCALER_PATH = "model/scaler.pkl"

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

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    df = pd.DataFrame([data], columns=FEATURE_COLUMNS)
    X_scaled = scaler.transform(df)
    prob = model.predict_proba(X_scaled)[0][1]

    return jsonify({
        "keylogger_probability": float(prob),
        "detected": prob >= 0.35
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
