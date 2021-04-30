from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import post_save
from videos.models import VideoStatus, Video
from videos.signals import video_publish_timestamp
from django.utils import timezone

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = VideoStatus.PUBLISH, publish_timestamp__lte = timezone.now())

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(Video, blank=True, related_name='playlist_featured', null=True, on_delete= models.SET_NULL)
    videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item', through='PlaylistItem')
    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices= VideoStatus.choices, default=VideoStatus.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    live = models.BooleanField(default=False)

    objects = PlaylistManager()

    def __str__(self):
        return self.title

        
    def save(self, *args, **kwargs):
        if self.status == VideoStatus.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.status == VideoStatus.DRAFT:
            self.publish_timestamp = None

        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


post_save.connect(video_publish_timestamp, sender=Playlist)

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['order', '-timestamp' ]