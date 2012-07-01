from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import SiteTestHelper
from video.factories import VideoFactory


class VideoTests(SiteTestHelper, TestCase):
    def test_video_index(self):
        VideoFactory()
        VideoFactory(name="Test Video 2", slug="video-2")
        self.assert_page_loads(reverse('video-index'),
            'video/video_index.html')

    def test_video_detail(self):
        video = VideoFactory()
        self.assert_page_loads(video.get_absolute_url(),
            'video/video_detail.html')

    def test_video_detail_is_not_published(self):
        video = VideoFactory(is_published=False)
        resp = self.client.get(video.get_absolute_url())
        self.assertEqual(resp.status_code, 404)
