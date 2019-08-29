import logging

import requests
from faker import Faker
from requests.exceptions import ConnectionError

from src.bot.settings import BOT_SETTINGS, SERVER_URL

log = logging.getLogger('Bot')


class Bot:
    # Bot for automated API usage
    faker = Faker()
    NUMBER_OF_USERS: int
    MAX_POSTS_PER_USER: int
    MAX_LIKES_PER_USER: int

    def __init__(self):
        self.users = dict()
        # Set every field from settings to the bot instance
        for key, val in BOT_SETTINGS.items():
            setattr(self, key, val)

    def create_users(self):
        log.info(f'Creating {self.NUMBER_OF_USERS} users')
        for _ in range(self.NUMBER_OF_USERS):
            username = self.faker.user_name()
            password = self.faker.password()
            data = {
                'username': username,
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name(),
                'email': self.faker.email(),
                'password': password,
            }
            response = requests.post(
                f'{SERVER_URL}/sign-up/', json=data
            )
            if not response.ok:
                log.error(f'Error signing up user {username}')
                quit(0)

            log.info(f'User {username} has signed up')
            self.users[username] = {'token': None, 'password': password}

    def get_tokens(self):
        log.info('Getting tokens for users')
        for username, user_data in self.users.items():
            payload = {
                'username': username,
                'password': user_data.get('password')
            }
            response = requests.post(f'{SERVER_URL}/token/', json=payload)
            if not response.ok:
                log.error(f'Error getting token for {username}')
                quit(0)

            user_data['token'] = response.json().get('access')
            log.info(f'Saved token for {username}')


if __name__ == '__main__':
    bot = Bot()
    try:
        requests.get(SERVER_URL)
    except ConnectionError:
        log.error('Did you start Django server?')
        log.error('Maybe your Server URL is different than in bot settings?')
        quit(0)

    bot.create_users()
    bot.get_tokens()
