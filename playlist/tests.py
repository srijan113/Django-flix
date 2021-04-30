from django.test import TestCase
from .models import Playlist
from videos.models import VideoStatus, Video
from django.utils import timezone

class VideoModelTestCase(TestCase):
    def setUp(self):
        video_a = Video.objects.create(title="This is title", video_id='abc234')
        self.video_a = video_a
        self.obj_a = Playlist.objects.create(title="video 1", description="This is just a day 1", video=video_a)
        self.obj_b = Playlist.objects.create(title="video 2", description="This is just a day 2", status=VideoStatus.PUBLISH, video=video_a)

    def test_video_playlist(self):
        qs = self.video_a.playlist_featured.all()
        self.assertEqual(qs.count(), 2)


    def test_video_playlist_ids_property(self):
        ids = self.obj_a.video.get_playlist_ids()
        actual_ids = list(Playlist.objects.filter(video = self.video_a).values_list('id', flat=True))
        self.assertEqual(len(ids), len(actual_ids))


    def test_valid_title(self):
        tittle = "video 1"
        qs = Playlist.objects.filter(title=tittle)
        self.assertTrue(qs.exists())

    def test_publish_case(self):
        now = timezone.now()
        qs_publish = Playlist.objects.filter(status=VideoStatus.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(qs_publish.exists())

    def test_live_case(self):
        qs = Playlist.objects.filter(live=False)
        self.assertTrue(qs.exists())

    def test_publish_manager(self):
        published_qs = Playlist.objects.published()
        self.assertTrue(published_qs.exists())