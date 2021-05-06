from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import post_save
from videos.models import VideoStatus, Video
from videos.signals import video_publish_timestamp
from django.utils import timezone
from categories.models import Category
from tags.models import TaggedItem

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = VideoStatus.PUBLISH, publish_timestamp__lte = timezone.now())

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Playlist(models.Model):
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = "TVS", "TV Show"
        SEASON = "SEA", "Season"
        PLAYLIST = "PLY", "Playlist"
    parent = models.ForeignKey("self", blank=True,null=True,on_delete = models.SET_NULL)
    category = models.ForeignKey(Category, related_name= 'playlists', null=True, blank=True, on_delete = models.SET_NULL)
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey(Video, blank=True, related_name='playlist_featured', null=True, on_delete= models.SET_NULL)
    videos = models.ManyToManyField(Video, blank=True, related_name='playlist_item', through='PlaylistItem')
    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices= VideoStatus.choices, default=VideoStatus.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    tags = GenericRelation(TaggedItem, related_query_name="playlist")

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


class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull = True, type = Playlist.PlaylistTypeChoices.SHOW)

class TVShowProxy(Playlist):

    objects = TVShowProxyManager()

    class Meta:
        proxy = True
        verbose_name = "TV Show"
        verbose_name_plural = "TV Shows"

    
    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args, **kwargs)


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type = Playlist.PlaylistTypeChoices.MOVIE)

class MovieProxy(Playlist):

    objects = MovieProxyManager()

    class Meta:
        proxy = True
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args, **kwargs)


class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull = False, type = Playlist.PlaylistTypeChoices.SEASON)

class TVShowSeasonProxy(Playlist):

    objects = TVShowSeasonProxyManager()

    class Meta:
        proxy = True
        verbose_name = "Season"
        verbose_name_plural = "Season"

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args, **kwargs)

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['order', '-timestamp' ]