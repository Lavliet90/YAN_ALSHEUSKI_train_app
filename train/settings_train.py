REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

CELERY_BROKER_URL = "redis://redis:6379/0"
RESULT_BACKEND = "redis://redis:6379/0"


STATIONS = [
    "Białystok",
    "Warszawa Centralna",
    "Kraków Główny",
    "Wrocław Główny",
    "Gdańsk Główny",
    "Poznań Główny",
    "Łódź Fabryczna",
    "Katowice",
    "Szczecin Główny",
    "Bydgoszcz Główna",
    "Lublin",
    "Zielona Góra",
    "Toruń Główny",
    "Rzeszów Główny",
    "Olsztyn Główny",
    "Gdynia Główna",
    "Kielce",
    "Opole Główne",
    "Częstochowa Główna",
    "Nowy Sącz",
]


CELERY_BEAT_SCHEDULE = {
    "broadcast-speed-every-10-seconds": {
        "task": "broadcast_speed",
        "schedule": 10.0,
    },
    "broadcast-station-every-180-seconds": {
        "task": "broadcast_station",
        "schedule": 180.0,
    },
}
