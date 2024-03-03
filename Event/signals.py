from celery.app import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, User
from django.core.mail import send_mail
from django.conf import settings
from .tasks import send_email_task


@receiver(post_save, sender=Event)
def create_event(sender, created, instance: Event, **kwargs):
    if not settings.TESTING:
        if created:
            users_notification = User.objects.filter(notify=True)
            for user in users_notification:
                send_email_task.delay("Уведомление",
                                      f"Уведомляем вас, что появилось новое событие  {instance.name} \n, "
                                      f"{instance.description} \n,"
                                      f"Мероприятие  проходит в {instance.meeting_time}",
                                      settings.EMAIL_HOST_USER,
                                      [user.email],
                                      fail_silently=False)
