from django.test import TestCase

from utils import SiteTestHelper


class ConfigTests(SiteTestHelper, TestCase):
    def test_config_present(self):
        resp = self.client.get('/')

        self.assertTrue(resp.context['config'])
