from django.test import TestCase
from stories.factories import StoryFactory
from video.factories import VideoFactory


class FrontTests(TestCase):
    def test_index_front(self):
        video = VideoFactory()
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['latest_video'], video)
