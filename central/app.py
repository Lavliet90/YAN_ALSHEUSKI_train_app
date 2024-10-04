from flask import Flask
import requests
import logging
from datetime import datetime
import redis
import threading
import pytz
from settings_central import (
    GATEKEEPER_URL,
    SLOW_LOG,
    NORMAL_LOG,
    FAST_LOG,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    FLASK_PORT,
    FLASK_HOST,
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

poland_tz = pytz.timezone("Europe/Warsaw")


def log_speed(filename, speed, timestamp):
    try:
        with open(filename, "a") as f:
            f.write(f"{timestamp.isoformat()}: {speed}\n")
        logging.info(f"Logged speed: {speed} in {filename}")
    except Exception as e:
        logging.error(f"Failed to log speed: {e}")


def handle_speed_message(message):
    speed = float(message["data"])
    current_time = datetime.now(poland_tz)

    if speed < 40:
        log_speed(SLOW_LOG, speed, current_time)
    elif 40 <= speed < 140:
        log_speed(NORMAL_LOG, speed, current_time)
    elif 140 <= speed <= 180:
        log_speed(FAST_LOG, speed, current_time)


def handle_station_message(message):
    station = message["data"].decode("utf-8")
    current_time = datetime.now(poland_tz)
    logging.info(
        f"Train approaching station: {station} at {current_time.isoformat()}"
    )

    try:
        gate_response = requests.get(GATEKEEPER_URL)
        gate_response.raise_for_status()

        gate_status = gate_response.json()
        if gate_status["status"]:
            logging.info("Gate is open. Requesting to lower the gate.")
            requests.post(GATEKEEPER_URL, json={"status": False})
            threading.Timer(10.0, raise_gate).start()
        else:
            logging.error("Gate is closed. No action taken.")
    except requests.RequestException as e:
        logging.error(f"Failed to check gate status: {e}")


def raise_gate():
    try:
        requests.post(GATEKEEPER_URL, json={"status": True})
        logging.info("Raising gate after 10 seconds.")
    except requests.RequestException as e:
        logging.error(f"Failed to raise gate: {e}")


def listen_to_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(
        **{
            "train_speed": handle_speed_message,
            "train_station": handle_station_message,
        }
    )
    pubsub.run_in_thread(sleep_time=0.001)


listen_to_redis()

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
