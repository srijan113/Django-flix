from django.db import models
from django.utils.text import slugify


class Video(models.Model):
    class VideoStatus(models.TextChoices):
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DU', 'Draft'
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=VideoStatus.choices, default=VideoStatus.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    live = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class AllVideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = "All Videos"


class PublishedVideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = "Published Videos"


class LiveVideoProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Live Video'
        verbose_name_plural = 'Live Videos'