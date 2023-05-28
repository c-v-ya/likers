import logging.config

from django.conf import settings

LOGGING = settings.LOGGING
LOGGING["loggers"] = {
    "": {
        "handlers": ["console", "file"],
        "level": "INFO",
        "propagate": True,
    },
}
logging.config.dictConfig(LOGGING)

SERVER_URL = "http://0.0.0.0:8000/api"

BOT_SETTINGS = {
    "NUMBER_OF_USERS": 5,
    "MAX_POSTS_PER_USER": 7,
    "MAX_LIKES_PER_USER": 4,
}
