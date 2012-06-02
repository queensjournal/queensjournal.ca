from django.utils.unittest import TestCase
from django.test.client import Client
from config.factories import SiteConfigFactory


class ConfigTests(TestCase):

    def setUp(self):
        self.config = SiteConfigFactory
        self.client = Client()

    def test_config_present(self):
        resp = self.client.get('/')

        self.assertEqual(len(response.context['config']), 1)
