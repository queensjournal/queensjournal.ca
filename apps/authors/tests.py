from django.test import TestCase

from utils import SiteTestHelper
from authors.factories import AuthorFactory


class MastheadTests(SiteTestHelper, TestCase):
    def test_author_detail(self):
        self.author = AuthorFactory()
        self.assert_page_loads(self.author.get_absolute_url(),
            'authors/author_detail.html')
