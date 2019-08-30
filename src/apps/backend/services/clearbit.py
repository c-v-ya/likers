import logging

import clearbit

from src.apps.backend.models import User

log = logging.getLogger(__file__)


class ClearBit:
    # Class, communicating with Clearbit Enrichment API

    @classmethod
    def enrich_user(cls, user: User):
        # Simple enrichment of user first and last name.
        # In real project could be more fields to parse.
        data = cls.find_person(user.email)
        if not data:
            return
        if data.get('name'):
            first_name = data['name'].get('givenName')
            last_name = data['name'].get('familyName')
            if first_name and not user.first_name:
                user.first_name = first_name
            if last_name and not user.last_name:
                user.last_name = last_name

            user.save(update_fields=['first_name', 'last_name'])

    @classmethod
    def find_person(cls, email: str):
        response = cls._make_request(email)
        if not response:
            log.info(f'No data found for {email}')
            return

        # Response could be 'pending' so in real scenario there would be
        # a callback url, handling this case. For now we just check for a field.
        if not response['person']:
            log.info(f'Person not found for {email}')
            return

        return response['person']

    @staticmethod
    def _make_request(email: str):
        try:
            return clearbit.Enrichment.find(email=email)
        except Exception as e:
            log.error(e)
            return
