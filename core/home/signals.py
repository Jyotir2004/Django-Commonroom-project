from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MemberStatus


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_status(sender, instance, created, **kwargs):
    if created:
        MemberStatus.objects.create(user=instance)
