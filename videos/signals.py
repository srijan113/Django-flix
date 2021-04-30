from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import  Video, AllVideoProxy, VideoStatus
from django.utils import timezone



@receiver(pre_save, sender=Video)
def video_publish_timestamp(sender, instance, *args, **kwargs):
    if instance.status == VideoStatus.PUBLISH and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()
    elif instance.status == VideoStatus.DRAFT:
        instance.publish_timestamp = None


