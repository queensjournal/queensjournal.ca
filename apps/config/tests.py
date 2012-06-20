from django.test import TestCase

from utils import SiteTestHelper
from video.factories import VideoFactory


class ConfigTests(SiteTestHelper, TestCase):
    def test_config_present(self):
        VideoFactory()
        resp = self.client.get('/')

        self.assertTrue(resp.context['config'])
