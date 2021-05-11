from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class VideoStatus(models.TextChoices):
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DU', 'Draft'

class VideoQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = VideoStatus.PUBLISH, publish_timestamp__lte = timezone.now())

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()



class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=VideoStatus.choices, default=VideoStatus.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    live = models.BooleanField(default=False)

    objects = VideoManager()

    def __str__(self):
        return self.title

    def get_video_id(self):
        if not self.is_published:
            return None
        return self.video_id
    
    @property
    def is_published(self):
        state = self.status
        if state != VideoStatus.PUBLISH:
            return False
        pub_timestamp = self.publish_timestamp
        if pub_timestamp is None:
            return False
        now = timezone.now()
        return pub_timestamp <= now 

    def save(self, *args, **kwargs):
        if self.status == VideoStatus.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.status == VideoStatus.DRAFT:
            self.publish_timestamp = None

        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        
    def get_playlist_ids(self):
        return self.playlist_featured.all().values_list('id', flat = True)

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