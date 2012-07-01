import datetime
from django.test import TestCase

from utils import SiteTestHelper
from video.factories import VideoFactory


class FrontTests(SiteTestHelper, TestCase):
    def setUp(self):
        super(FrontTests, self).setUp()
        self.video = VideoFactory()

    def test_index_front(self):
        self.assert_page_loads('/')

    def test_front_video_is_latest(self):
        self.video = VideoFactory(pub_date=datetime.datetime.now())
        resp = self.client.get('/')
        self.assertEqual(resp.context['latest_video'], self.video)
