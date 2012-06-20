import datetime
from django.test import TestCase

from utils import SiteTestHelper
from video.factories import VideoFactory


class FrontTests(SiteTestHelper, TestCase):
    def test_index_front(self):
        self.video = VideoFactory()
        self.assert_page_loads('/', 'front.html')

    def test_front_video_is_latest(self):
        self.video = VideoFactory(pub_date=datetime.datetime.now())
        resp = self.client.get('/')
        self.assertEqual(resp.context['latest_video'], self.video)
