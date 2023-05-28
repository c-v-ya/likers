import logging

import requests
from requests import ConnectionError

from bot import settings
from bot.bot import Bot

log = logging.getLogger(__file__)

if __name__ == "__main__":
    try:
        requests.get(settings.SERVER_URL)
    except ConnectionError:
        log.error(
            "Did you start Django server? Maybe your Server URL is different than in bot settings?"
        )
        quit(0)

    Bot().complete_flow()
