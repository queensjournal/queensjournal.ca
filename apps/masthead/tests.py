from django.test import TestCase

from utils import SiteTestHelper
from structure.factories import AuthorFactory


class MastheadTests(SiteTestHelper, TestCase):
    def test_author_detail(self):
        self.author = AuthorFactory()
        self.assert_page_loads(self.author.get_absolute_url(),
            'masthead/author_detail.html')
