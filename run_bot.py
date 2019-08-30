import logging

import requests
from requests import ConnectionError

from src.bot import settings
from src.bot.bot import Bot

log = logging.getLogger(__file__)

if __name__ == '__main__':
    bot = Bot()
    try:
        requests.get(settings.SERVER_URL)
    except ConnectionError:
        log.error('Did you start Django server?')
        log.error('Maybe your Server URL is different than in bot settings?')
        quit(0)

    bot.create_users()
    bot.get_tokens()
    bot.perform_posting()
    bot.perform_liking()
