from django.test import TestCase

from utils import SiteTestHelper
from video.factories import VideoFactory


class FrontTests(SiteTestHelper, TestCase):
    def setUp(self):
        super(FrontTests, self).setUp()
        self.video = VideoFactory()

    def test_index_front(self):
        self.assert_page_loads('/')
