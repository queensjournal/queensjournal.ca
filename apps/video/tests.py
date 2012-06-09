from django.test import TestCase
from django.core.urlresolvers import reverse

from video.factories import VideoFactory


class VideoTests(TestCase):

    def test_video_index(self):
        VideoFactory()
        VideoFactory(name="Test Video 2", slug="video-2")
        resp = self.client.get(reverse('video-index'))
        self.assertEqual(resp.status_code, 200)

    def test_video_detail(self):
        video = VideoFactory()
        resp = self.client.get(video.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_video_detail_is_not_published(self):
        video = VideoFactory(is_published=False)
        resp = self.client.get(video.get_absolute_url())
        self.assertEqual(resp.status_code, 404)
