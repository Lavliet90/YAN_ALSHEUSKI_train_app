from flask import Flask
from celery import Celery
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["result_backend"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    return celery


app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["result_backend"] = "redis://redis:6379/0"
app.config["beat_schedule"] = {
    "broadcast-speed-every-10-seconds": {
        "task": "broadcast_speed",
        "schedule": 10.0,
    },
    "broadcast-station-every-180-seconds": {
        "task": "broadcast_station",
        "schedule": 18.0,
    },
}

celery = make_celery(app)

STATIONS = ["Station1", "Station2", "Station3", "Station4"]  # Добавьте до 20 станций


@app.route("/")
def index():
    logger.info("KOK")
    return "Train Service Running"


@celery.task(name="broadcast_speed")
def broadcast_speed():
    speed = random.uniform(0, 180)
    logger.info(f"Broadcasting speed: {speed}")
    return speed


@celery.task(name="broadcast_station")
def broadcast_station():
    station = random.choice(STATIONS)
    logger.info(f"Broadcasting station: {station}")
    return station
