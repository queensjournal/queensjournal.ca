from django.test import TestCase

from utils import SiteTestHelper


class FrontTests(SiteTestHelper, TestCase):
    def test_index_front(self):
        self.assert_page_loads('/', 'front.html')
