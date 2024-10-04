from flask import Flask
from celery import Celery
from settings_train import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    CELERY_BROKER_URL,
    RESULT_BACKEND,
    STATIONS,
    CELERY_BEAT_SCHEDULE,
)
import random
import logging
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["result_backend"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    return celery


app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
app.config["result_backend"] = RESULT_BACKEND
app.config["beat_schedule"] = CELERY_BEAT_SCHEDULE

celery = make_celery(app)


@celery.task(name="broadcast_speed")
def broadcast_speed():
    speed = random.uniform(0, 180)
    logger.info(f"Broadcasting speed: {speed}")
    redis_client.publish("train_speed", speed)
    return speed


@celery.task(name="broadcast_station")
def broadcast_station():
    station = random.choice(STATIONS)
    logger.info(f"Broadcasting station: {station}")
    redis_client.publish("train_station", station)
    return station
