from django.test import TestCase

from apps.tests import SiteTestHelper
from video.factories import VideoFactory


class FrontTests(SiteTestHelper, TestCase):
    def test_index_front(self):
        video = VideoFactory()
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['latest_video'], video)
