from django.apps import AppConfig
from django.db.models.signals import post_save


class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Event'

    def ready(self):
        from .signals import create_event
        from .models import Event
        post_save.connect(create_event, sender=Event)
