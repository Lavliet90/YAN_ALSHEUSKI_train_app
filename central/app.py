from flask import Flask, request, jsonify
import requests
import logging
from datetime import datetime, timezone
import redis
import threading

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

GATEKEEPER_URL = "http://gatekeeper:5001/gate/status"
SLOW_LOG = "logs/slow.log"
NORMAL_LOG = "logs/normal.log"
FAST_LOG = "logs/fast.log"

redis_client = redis.Redis(host='redis', port=6379, db=0)


def log_speed(filename, speed, timestamp):
    with open(filename, 'a') as f:
        f.write(f"{timestamp.isoformat()}: {speed}\n")
    logging.info(f"Logged speed: {speed} in {filename}")


def handle_speed_message(message):
    speed = float(message['data'])
    current_time = datetime.now(timezone.utc)

    if speed < 40:
        log_speed(SLOW_LOG, speed, current_time)
    elif 40 <= speed < 140:
        log_speed(NORMAL_LOG, speed, current_time)
    elif 140 <= speed <= 180:
        log_speed(FAST_LOG, speed, current_time)


def handle_station_message(message):
    station = message['data'].decode('utf-8')
    current_time = datetime.now(timezone.utc)
    logging.info(f"Train approaching station: {station} at {current_time.isoformat()}")

    gate_response = requests.get(GATEKEEPER_URL)

    if gate_response.status_code == 200:
        gate_status = gate_response.json()
        if gate_status['status']:
            logging.info("Gate is open. Requesting to lower the gate.")
            requests.post(GATEKEEPER_URL, json={"status": False})
            threading.Timer(10.0, raise_gate).start()
        else:
            logging.error("Gate is closed. No action taken.")
    else:
        logging.error("Failed to check gate status.")


def raise_gate():
    requests.post(GATEKEEPER_URL, json={"status": True})
    logging.info("Raising gate after 10 seconds.")


def listen_to_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(
        **{
            "train_speed": handle_speed_message,
            "train_station": handle_station_message
        }
    )
    pubsub.run_in_thread(sleep_time=0.001)


listen_to_redis()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
