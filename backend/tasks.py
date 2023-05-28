import logging

from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task
def enrich(user_id: int):
    user = get_user_model().objects.filter(id=user_id).first()
    if user:
        logging.info(f"User {user.id} enriched")
