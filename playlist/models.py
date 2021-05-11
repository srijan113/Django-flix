from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, Max, Min, Q
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import post_save
from videos.models import VideoStatus, Video
from videos.signals import video_publish_timestamp
from django.utils import timezone
from categories.models import Category
from tags.models import TaggedItem
from ratings.models import Rating

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = VideoStatus.PUBLISH, publish_timestamp__lte = timezone.now())

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured_playlist(self):
        return self.get_queryset().filter(type = Playlist.PlaylistTypeChoices.PLAYLIST)


class Playlist(models.Model):
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = "TVS", "TV Show"
        SEASON = "SEA", "Season"
        PLAYLIST = "PLY", "Playlist"
    parent = models.ForeignKey("self", blank=True,null=True,on_delete = models.SET_NULL)
    related = models.ManyToManyField("self", blank= True, related_name = 'related', through='PlaylistRelated')
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
    ratings = GenericRelation(Rating, related_query_name='playlist')

    objects = PlaylistManager()

    def __str__(self):
        return self.title
    

    def get_related_items(self):
        return self.playlistrelated_set.all()

    def get_absolute_url(self):
        if self.is_movie:
            return f"/movies/{self.slug}/"
        if self.is_show:
            return f"/show/{self.slug}/"
        if self.is_season:
            return f"/show/{self.parent.slug}/season/{self.slug}"
        return f"playlist/{self.slug}"



    @property
    def is_season(self):
        return self.type == Playlist.PlaylistTypeChoices.SEASON  
    
    @property
    def is_movie(self):
        return self.type == Playlist.PlaylistTypeChoices.MOVIE

    @property
    def is_show(self):
        return self.type == Playlist.PlaylistTypeChoices.SHOW


    def get_avg_rating(self):
        return Playlist.objects.filter(id = self.id).aggregate(average = Avg("ratings__value"))

    def get_rating_spread(self):
        return Playlist.objects.filter(id = self.id).aggregate(max = Max("ratings__value"), min = Min("ratings__value"))

    def get_short_description(self):
        return ""

    def get_video_id(self):
        """
        gets the main if for the TV show for example The office for the mulitple season with multiplel videos in it

        """
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        """
            gets  your the clip that are related to the playlist 
        """
        return self.playlistitem_set.all().published()
        
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

    @property
    def seasons(self):
        return self.playlist_set.published()
         
    def get_short_description(self):
        return f'{self.seasons.count()} Season' 


    def get_video_id(self):
        """
            gets the main if for the TV show for example The office for the mulitple season with multiplel videos in it
        """
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        """
            gets the clips again for the movies
        """
        return self.playlistitem_set.all().published()


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type = Playlist.PlaylistTypeChoices.MOVIE)

class MovieProxy(Playlist):

    objects = MovieProxyManager()

    def get_movie_id(self):
        """
        get the movies id like linked video direct movies
        """
        return self.get_video_id(self)

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

    def get_season_trailer(self):
        """
            get the each season trailer to the user
        """
        return self.get_video_id(self)

    def get_episodes(self):
        """
            gets  your the episode that are related to the TVshow 
        """
        return self.playlistitem_set.all().published()


class PlaylistItemQuerySet(models.QuerySet):
    def published(self):
        return self.filter(playlist__status = VideoStatus.PUBLISH, 
                            playlist__publish_timestamp__lte = timezone.now(), 
                            video__status = VideoStatus.PUBLISH, 
                            video__publish_timestamp__lte = timezone.now()
                            )

class PlaylistItemManager(models.Manager):
    def get_queryset(self):
        return PlaylistItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published() 


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add= True)

    objects = PlaylistItemManager()

    class Meta:
        ordering = ['order', '-timestamp']



def playlistRelatedLimitTo():
    return Q(type = Playlist.PlaylistTypeChoices.MOVIE) | Q(type = Playlist.PlaylistTypeChoices.SHOW)


class PlaylistRelated(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    related = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name= 'related_item', limit_choices_to= playlistRelatedLimitTo)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add= True)
    