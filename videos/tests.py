from django.test import TestCase
from .models import Video, VideoStatus
from django.utils import timezone

class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="video 1", description="This is just a day 1", video_id='1235')
        Video.objects.create(title="video 2", description="This is just a day 2", video_id='3456', status=VideoStatus.PUBLISH)

    def test_valid_title(self):
        tittle = "video 1"
        qs = Video.objects.filter(title=tittle)
        self.assertTrue(qs.exists())

    def test_publish_case(self):
        now = timezone.now()
        qs_publish = Video.objects.filter(status=VideoStatus.PUBLISH, publish_timestamp__lte=now)
        self.assertTrue(qs_publish.exists())

    def test_live_case(self):
        qs = Video.objects.filter(live=False)
        self.assertTrue(qs.exists())

    def test_publish_manager(self):
        published_qs = Video.objects.published()
        self.assertTrue(published_qs.exists())