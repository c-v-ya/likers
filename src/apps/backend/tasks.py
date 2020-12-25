from celery import shared_task
from django.contrib.auth import get_user_model

from src.apps.backend.services.clearbit import ClearBit


@shared_task
def enrich(user_id: int):
    user = get_user_model().objects.filter(id=user_id).first()
    if user:
        ClearBit.enrich_user(user)
    return 0
